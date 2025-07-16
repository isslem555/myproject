# services.py
import requests
from datetime import datetime

test_history = []

def run_endpoint_test(data):
    method = data.get('method', 'GET')
    url = data.get('url', '')
    params = data.get('params', {})
    path_vars = data.get('path_vars', {})
    body = data.get('body', {})
    headers = data.get('headers', {})

    if 'api.nasa.gov' in url and 'api_key' not in params:
        return {
            'status': 'error',
            'error': 'Clé API NASA (api_key) requise pour cet endpoint'
        }

    formatted_url = url
    for key, value in path_vars.items():
        formatted_url = formatted_url.replace(f'{{{key}}}', value)

    try:
        response = requests.request(
            method,
            formatted_url,
            params=params,
            json=body if body else None,
            headers=headers,
            timeout=5
        )

        if 200 <= response.status_code <= 299:
            test_status = "succeeded" if response.status_code == 201 else "passed"
        else:
            test_status = "failed"

        test_entry = {
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'url': formatted_url,
            'params': params,
            'path_vars': path_vars,
            'body': body,
            'headers': headers,
            'status_code': response.status_code,
            'response': response.text,
            'test_status': test_status
        }
        test_history.append(test_entry)

        return {
            'status': 'success',
            'status_code': response.status_code,
            'response': response.text,
            'request_body': body
        }

    except requests.RequestException as e:
        test_entry = {
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'url': formatted_url,
            'params': params,
            'path_vars': path_vars,
            'body': body,
            'headers': headers,
            'status_code': 500,
            'response': str(e),
            'test_status': 'failed'
        }
        test_history.append(test_entry)

        return {
            'status': 'error',
            'error': str(e)
        }

def get_test_history():
    return test_history
