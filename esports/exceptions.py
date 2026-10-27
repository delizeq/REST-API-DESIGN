from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    if response.status_code == 400:
        response.data = {'error': 'Некоректні дані.', 'details': response.data}
    else:
        detail = response.data.get('detail') if isinstance(response.data, dict) else None
        response.data = {'error': str(detail) if detail else 'Помилка запиту.'}
    return response