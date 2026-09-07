from django.contrib import admin
from .models import Categories, Article, About, Comment

# Customize Django Admin Header
admin.site.site_header = "MyBlog Super Admin Portal"
admin.site.site_title = "MyBlog Admin"
admin.site.index_title = "Welcome to the Super Admin Dashboard"

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_feature', 'created_at')
    search_fields = ('id', 'title', 'category__category_name', 'status', 'author__username')
    list_editable = ('status', 'is_feature')
    list_filter = ('author', 'category', 'status', 'is_feature')
    
    # Automatically assign the logged-in user as author if not set
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_at', 'updated_at')
    search_fields = ('category_name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('user', 'article')
    search_fields = ('user__username', 'comment', 'article__title')

class AboutAdmin(admin.ModelAdmin):
    list_display = ('heading', 'created_at')
    
    def has_add_permission(self, request):
        # Only allow 1 About page detail to be created
        count = About.objects.all().count()
        if count == 0:
            return True
        return False

admin.site.register(Categories, CategoryAdmin)
admin.site.register(Article, BlogAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(Comment, CommentAdmin)
