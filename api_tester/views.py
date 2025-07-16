# api_tester/views.py

import json
import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from scraping_data.models import SwaggerProject
from .models import TestResult


def tester_page(request, project_pk):
    """
    Affiche la page du testeur d'API pour le projet donné.
    """
    project = get_object_or_404(SwaggerProject, pk=project_pk)
    context = {
        'project': project,
        'initial_data': json.dumps(request.GET.dict())
    }
    return render(request, 'api_tester/tester_page.html', context)


@csrf_exempt
def test_endpoint(request, project_pk):
    """
    Reçoit la requête Ajax depuis le formulaire de testeur
    et effectue l'appel HTTP réel à l'API cible.
    """
    project = get_object_or_404(SwaggerProject, pk=project_pk)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'error': 'Corps JSON invalide.'}, status=400)

    method = data.get('method', 'GET')
    url = data.get('url', '')
    params = data.get('params', {})
    path_vars = data.get('path_vars', {})
    body = data.get('body', {})
    headers = data.get('headers', {})

    # Remplace les variables dans l'URL
    formatted_url = url
    for key, value in path_vars.items():
        formatted_url = formatted_url.replace(f'{{{key}}}', str(value))

    try:
        response = requests.request(
            method=method,
            url=formatted_url,
            params=params,
            json=body if body else None,
            headers=headers,
            timeout=10
        )

        test_status = "passed" if 200 <= response.status_code <= 299 else "failed"

        # Sauvegarde du résultat du test en base
        TestResult.objects.create(
            project=project,
            method=method,
            url=formatted_url,
            status_code=response.status_code,
            response_body=response.text,
            test_status=test_status
        )

        return JsonResponse({
            'status': 'success',
            'status_code': response.status_code,
            'response': response.text,
            'request_body': body
        })

    except requests.RequestException as e:
        # Sauvegarde aussi l'erreur dans les résultats
        TestResult.objects.create(
            project=project,
            method=method,
            url=formatted_url,
            status_code=500,
            response_body=str(e),
            test_status='failed'
        )

        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)


def download_history(request, project_pk):
    """
    Télécharge l'historique complet des tests sous forme de fichier JSON.
    """
    project = get_object_or_404(SwaggerProject, pk=project_pk)
    history_queryset = project.test_results.all().values(
        'timestamp', 'method', 'url', 'status_code', 'response_body', 'test_status'
    )
    history_list = list(history_queryset)

    for item in history_list:
        if 'timestamp' in item and hasattr(item['timestamp'], 'isoformat'):
            item['timestamp'] = item['timestamp'].isoformat()

    json_content = json.dumps(history_list, indent=2)
    response = HttpResponse(json_content, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="test_history_project_{project.pk}.json"'
    return response


def simple_test_view(request):
    """
    Une vue ultra-simple qui rend simplement un template pour tester l'affichage.
    """
    return render(request, 'api_tester/simple_test.html')


