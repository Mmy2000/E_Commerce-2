from .models import Category


def menu_links(request):
    links = Category.objects.all()[:10]
    return dict(links=links)