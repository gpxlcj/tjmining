from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin, AdminMarkdownWidget, MarkdownField
from models import BlogModel, CommentModel, ImageModel

class BlogAdmin(MarkdownModelAdmin):
    list_display = ('title', 'create_time', 'author', 'blog_id')
    search_fields = ('title', 'author')
    readonly_fields = ('blog_id',)
    formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}

class CommentAdmin(admin.ModelAdmin):
    list_display =  ('create_time', 'author')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'width')

admin.site.register(BlogModel, BlogAdmin)
admin.site.register(CommentModel, CommentAdmin)
admin.site.register(ImageModel, ImageAdmin)