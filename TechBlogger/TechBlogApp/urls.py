from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("content/<slug:slug>",post_content,name="post_content"),
    path("category/<str:name>",category_content,name="category"),
    path("sections/<str:name>",sections,name="sections"),
    path("load_more_posts/",load_more_posts,name="load_more_posts"),
    path("posts/",blog_post,name="blogpost"),
    path("about/",About,name="about"),
    path("contact/",contact_us,name="contact"),
]