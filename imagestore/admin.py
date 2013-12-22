from django.contrib import admin
from imagestore.models import Image, Album, AlbumUpload
from sorl.thumbnail.admin import AdminImageMixin, AdminInlineImageMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class InlineImageAdmin(AdminInlineImageMixin, admin.TabularInline):
    model = Image
    fieldsets = ((None, {'fields': ['image', 'title', 'featured', 'user', 'order', 'tags', 'album']}),)
    raw_id_fields = ('user', )
    extra = 0

class AlbumAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['name', 'user', 'is_public', 'order']}),)
    list_display = ('name', 'admin_thumbnail','user', 'created', 'updated', 'is_public', 'order')
    list_editable = ('order', )
    inlines = [InlineImageAdmin]

admin.site.register(Album, AlbumAdmin)

class ImageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fieldsets = (
            (None, {'fields': ['title', 'image', 'description', 'featured', 'tags', 'album']}),
            (_('Advanced options'), {'fields': ['related_images', 'related_articles', 'created', 'user', 'order'], 'classes': ['collapse']}))
    list_display = ('admin_thumbnail', 'title', 'featured', 'album', 'tags', 'order',  'created')
    list_filter = ('album', 'featured')
    list_editable = ('title', 'album', 'featured', 'tags', 'order', 'created')
    raw_id_fields = ('user', )
    filter_horizontal = ('related_images', 'related_articles')
    search_fields = ('title', 'album__name', 'description', 'tags')

class AlbumUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

IMAGE_MODEL = getattr(settings, 'IMAGESTORE_IMAGE_MODEL', None)
if not IMAGE_MODEL:
    admin.site.register(Image, ImageAdmin)

ALBUM_MODEL = getattr(settings, 'IMAGESTORE_ALBUM_MODEL', None)
if not ALBUM_MODEL:
    admin.site.register(AlbumUpload, AlbumUploadAdmin)
