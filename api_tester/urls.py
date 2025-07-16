# api_tester/urls.py

from django.urls import path
from . import views

app_name = 'api_tester'

urlpatterns = [
    path(
        '<int:project_pk>/tester/',
        views.tester_page,
        name='tester_page'
    ),
    path(
        '<int:project_pk>/test-endpoint/',
        views.test_endpoint,
        name='test_endpoint'
    ),
    path(
        '<int:project_pk>/download-history/',
        views.download_history,
        name='download_history'
    ),
    path(
        'simple-test/',
        views.simple_test_view,
        name='simple_test'
    ),
]
