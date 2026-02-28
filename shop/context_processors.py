from .models import Product


def compare_context(request):
    """Добавляет информацию о сравнении в контекст"""
    compare_list = request.session.get('compare_list', [])
    compare_count = len(compare_list)
    
    return {
        'compare_count': compare_count,
        'compare_list': compare_list,
    }
