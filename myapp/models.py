from django.db import models
from django.utils.text import slugify 
from django.contrib.auth.models import User

class Categories(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.category_name
    
STATUS_CHOICES=(
    ('Draft','Draft'),
    ('Published','Published')
)

class Article(models.Model):
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='articles')
    title=models.CharField(max_length=100,unique=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='articles')
    slug=models.SlugField(max_length=200,blank=True,unique=True)
    featured_image = models.ImageField(upload_to='articles/%Y/%m/%d')
    short_description=models.CharField(max_length=500)
    blogbody=models.TextField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="Draft")
    is_feature=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)




def save(self, *args, **kwargs):
    self.slug = slugify(self.title)
    super().save(*args, **kwargs)

def __str__(self):
    return self.title
    

class About(models.Model):
    heading = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='about/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)




    def __str__(self):
        return self.comment
