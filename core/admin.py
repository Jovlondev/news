from django.contrib import admin
from .models import Category,Contact,New,Comment,Subscribe
# Register your models here.
class NewsInline(admin.StackedInline):
    model = New
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    inlines = [NewsInline]



admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(New)
admin.site.register(Subscribe)