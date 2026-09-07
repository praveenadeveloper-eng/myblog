from . models import Categories


def get_categories(request):
    categories=Categories.objects.all()
    return dict(categories=categories)