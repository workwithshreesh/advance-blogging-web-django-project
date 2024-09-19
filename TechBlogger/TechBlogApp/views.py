from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.core.paginator import Paginator
from .models import *
from django.db.models import Count
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def home(request):
    popular_post = Post.objects.filter(section="Popular",status="1").order_by("-id")[0:4]
    recent_post = Post.objects.filter(section="Recent",status="1").order_by("-id")[0:4]
    main_post = Post.objects.filter(main_post=True,status="1")[0:1]
    editors_pic = Post.objects.filter(section = "Editors-Pic",status="1").order_by("-id")
    trending = Post.objects.filter(section = "Trending",status="1").order_by("-id")
    inspiration = Post.objects.filter(section = "Inspiration",status="1").order_by("-id")[0:2]
    latestPost = Post.objects.filter(section = "Latest-Post",status="1").order_by("-id")[0:4]
    
    context = {"popular_post":popular_post,"recent_post":recent_post,"main_post":main_post,"editors_pic":editors_pic,
               "trending":trending,"inspiration":inspiration,"LatestPost":latestPost}
    return render(request,"Main/index.html",context)




def post_content(request,slug):
    
    postContent = Post.objects.get(slug=slug)
    tags = Tag.objects.filter(post=postContent)
    popular_post = Post.objects.filter(section="Popular",status="1").order_by("-id")[0:4]
    allSections = Post.objects.values('section').filter(status="1").annotate(post_count=Count('section')).distinct()
    
    context = {"single_post":postContent,
               "tags":tags,
               "popular_post":popular_post,
               "allsection":allSections}
    return render(request,"blog-single.html",context)




def category_content(request,name):
    cat = get_object_or_404(Category, name=name)  # Get the specific category by name
    posts = Post.objects.filter(Category=cat,status="1")  # Get all posts related to this category
    allSections = Post.objects.values('section').filter(status="1").annotate(post_count=Count('section')).distinct()
    popular_post = Post.objects.filter(section="Popular",status="1").order_by("-id")[0:4]
    latestPost = Post.objects.filter(section = "Latest-Post",status="1").order_by("-id")[0:4]
    
    paginator = Paginator(posts,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"cat": cat, "posts": posts,"allSection":allSections,
               "popular_post":popular_post,"latestPost":latestPost,"page_obj":page_obj}  # Pass both the category and related posts to the template
    return render(request, "category.html", context)





def sections(request,name):
    post = Post.objects.filter(section = name)
    posts = Post.objects.all().order_by("-id")[:6]
    popular_post = Post.objects.filter(section="Popular",status="1").order_by("-id")[0:4]
    trending = Post.objects.filter(section = "Trending",status="1").order_by("-id")[:1]
    allSections = Post.objects.values('section').filter(status="1").annotate(post_count=Count('section')).distinct()
    
    paginator = Paginator(post,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"secposts":page_obj, "trending":trending,'allSections':allSections,
               "popularpost":popular_post,"posts":posts}
    return render(request,"personal.html",context)




def load_more_posts(request):
    offset = int(request.GET.get('offset',0))
    limit = int(request.GET.get('limit',4))
    
    posts = Post.objects.filter(section = "Latest-Post",status="1").order_by("-id")[offset:offset + limit]
    posts_data = []
    for post in posts:
        posts_data.append({
            'title': post.title,
            'slug': post.slug,
            'featured_image': post.featured_image.url,
            'author': post.author,
            'category': post.Category.name,
            'date': post.date.strftime('%B %d, %Y'),
            'content': post.content,
        })
    data = {
        "posts":posts_data
    }
    
    return JsonResponse(data)





def blog_post(request):
    post = Post.objects.filter(status = "1").order_by("-id")
    
    paginator = Paginator(post,5)
    page_number = request.GET.get('page')
    posts_obj = paginator.get_page(page_number)
    
    data = {
        "posts":posts_obj
    }
    return render(request,"minimal.html",data)



def About(request):
    allSections = Post.objects.values('section').filter(status="1").annotate(post_count=Count('section')).distinct()
    popular_post = Post.objects.filter(section="Popular",status="1").order_by("-id")[0:4]
    latestPost = Post.objects.filter(section = "Latest-Post",status="1").order_by("-id")[0:4]
    
    context = {"allSection":allSections,
               "popular_post":popular_post,"latestPost":latestPost}
    return render(request,"about.html",context)

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        subject = request.POST.get('InputSubject')
        message = request.POST.get('InputMessage')

        # Combine name and message for the email body
        full_message = f"Message from {name}:\n\n{message}"

        # Send email
        send_mail(
            subject,
            full_message,
            email,  # From the user's email
            [settings.CONTACT_EMAIL],  # To your configured email
            fail_silently=False,
        )

        # Redirect or inform the user after successful submission
        # return redirect('contact_success')  # Replace with your success URL
        return HttpResponse("Success")
    else:
        return render(request, 'contact.html')