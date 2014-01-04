from django.contrib import admin
from imagestore.models import Image, Album, AlbumUpload
from sorl.thumbnail.admin import AdminImageMixin, AdminInlineImageMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.forms import ModelForm
import datetime

def form_factory(form_model):
    class BaseForm(ModelForm):
        class Meta:
            model = form_model

        def __init__(self, *args, **kwargs):
            super(BaseForm, self).__init__(*args, **kwargs)
            self.fields['slug'].required = False

        def clean_slug(self):
            slug = self.cleaned_data['slug']
            if len(slug) == 0:
                title = ""
                if 'title' in self.cleaned_data:
                    title = self.cleaned_data['title']
                elif 'name' in self.cleaned_data:
                    title = self.cleaned_data['name']
                else:
                    raise Exception(_(u'Form model "%s" has no "title" or "name" fields.' % form_model))
                slug = slugify(title)
            if len(slug) == 0:
                slug = slugify('%s-%s' % (self.instance.pk, datetime.datetime.now()))

            return slug
    return BaseForm


class InlineImageAdmin(AdminInlineImageMixin, admin.TabularInline):
    model = Image
    fieldsets = ((None, {'fields': ['image', 'title', 'slug', 'tags', 'featured', 'created']}),)
    extra = 0

class AlbumAdmin(admin.ModelAdmin):
    form = form_factory(Album)
    fieldsets = ((None, {'fields': ['name', 'slug', 'is_public', 'order', 'user']}),)
    date_hierarchy = 'created'
    list_display = ('admin_thumbnail', 'name', 'slug', 'created', 'updated', 'is_public')
    list_editable = ('is_public', 'name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('is_public', 'user')
    inlines = [InlineImageAdmin]

admin.site.register(Album, AlbumAdmin)

class ImageAdmin(admin.ModelAdmin):
    form = form_factory(Image)
    date_hierarchy = 'created'
    fieldsets = (
            (None, {'fields': ['title', 'slug', 'image', 'description', 'featured', 'tags', 'album']}),
            (_('Advanced options'), {'fields': ['related_images', 'related_articles', 'created', 'user', 'order'], 'classes': ['collapse']}))
    list_display = ('admin_thumbnail', 'album', 'title', 'slug', 'tags',  'created', 'featured')
    list_filter = ('album', 'featured', 'user')
    list_editable = ('title', 'slug', 'album', 'featured', 'tags', 'created')
    raw_id_fields = ('user', )
    filter_horizontal = ('related_images', 'related_articles')
    search_fields = ('title', 'album__name', 'description', 'tags', 'slug')
    prepopulated_fields = {"slug": ("title",)}


class AlbumUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

IMAGE_MODEL = getattr(settings, 'IMAGESTORE_IMAGE_MODEL', None)
if not IMAGE_MODEL:
    admin.site.register(Image, ImageAdmin)

ALBUM_MODEL = getattr(settings, 'IMAGESTORE_ALBUM_MODEL', None)
if not ALBUM_MODEL:
    admin.site.register(AlbumUpload, AlbumUploadAdmin)
