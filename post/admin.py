from django.contrib import admin

from . import models

admin.site.register(models.PostImage)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'short_description', 'address', 'latitude', 'longitude', 'isReligious', 'isNature', 'isIndoor', 'isHistorical', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')

    def short_description(self, obj):
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    short_description.short_description = 'Description'

admin.site.register(models.Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
     list_display = ('user', 'post', 'body','approved', 'created_at')
     list_filter = ('approved', 'created_at')

admin.site.register(models.PostComment, CommentAdmin)

