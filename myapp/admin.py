from django.contrib import admin

from .models import Categories,Article,About,Comment


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=('title','category','author','status','is_feature')
    search_fields =('id','title','category__category_name','status')
    list_editable=('is_feature',)



class AboutAdmin(admin.ModelAdmin):
    def has_had_permission(self,equest):
        count = About.objects.all().count()
        if count == 0:
            return True
        return False

admin.site.register(Categories)
admin.site.register(Article,BlogAdmin)
admin.site.register(About,AboutAdmin)
admin.site.register(Comment)




