from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    status_choice = (
        ('0', 'Draft'),
        ('1', 'Publish'),
    )
    
    section_choice = (
        ('Editors-Pic', 'Editors-Pic'),
        ('Popular', 'Popular'),
        ('Recent', 'Recent'),
        ('Trending', 'Trending'),
        ('Inspiration', 'Inspiration'),
        ('Latest-Post', 'Latest-Post'),)
    
    
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to="images")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    content = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(choices=status_choice, max_length=100)
    section = models.CharField(choices=section_choice, max_length=100)
    main_post = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

# Connect the pre_save signal to the receiver function
pre_save.connect(pre_save_post_receiver, sender=Post)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
