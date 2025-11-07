from django.contrib import admin
from .models import Category,Contact,New,Comment,Subscribe, User
# Register your models here.
admin.site.register(User)


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