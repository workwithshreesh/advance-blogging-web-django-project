from .models import Category, Post

def categories_processor(request):
    categories = Category.objects.all()
    allSections = Post.objects.values('section').distinct()

    return {'allCategory': categories,"allSection":allSections}
