from django.contrib import admin
from django.template.defaultfilters import slugify 


from photostorage.models import Family, Group, Photo, PhotoGroup, PhotoTag, Tag

class PhotoGroupAdmin(admin.TabularInline):
    model = PhotoGroup
    min_num = 1

class PhotoTagAdmin(admin.TabularInline):
    model = PhotoTag
    min_num = 1
    
@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"
    exclude=("slug",)
    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"
    exclude=("slug",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug")
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"
    exclude=("slug",)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    @admin.display(description='тэги')
    def tags_list(self, obj):
        return list(tag for tag in obj.tag.all())

    @admin.display(description='группы')
    def groups_list(self, obj):
        return list(group for group in obj.group.all())
    
    list_display = (
        "pk", "image", "family", "created_date",
        "groups_list", "tags_list"
        )
    search_fields = (
        "family", "created_date","group", "tag"
        )
    list_filter = ("family", "created_date", "group", "tag")
    empty_value_display = "-пусто-"
    inlines = [PhotoGroupAdmin,
               PhotoTagAdmin]