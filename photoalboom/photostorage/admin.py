from django.contrib import admin
from django.template.defaultfilters import slugify 


from photostorage.models import Family, Group, Photo, PhotoGroup, PhotoTag, Tag

class PhotoGroupAdmin(admin.TabularInline):
    model = PhotoGroup
    min_num = 0

class PhotoTagAdmin(admin.TabularInline):
    model = PhotoTag
    min_num = 0
    
@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    @admin.display(description='участники')
    def members_list(self, obj):
        return list(member for member in obj.members.all())
    
    list_display = ("pk", "title", "slug", "creator", "members_list")
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
        return list(tag for tag in obj.tags.all())
    
    @admin.display(description='families')
    def families_list(self, obj):
        return list(family for family in obj.families.all())

    @admin.display(description='группы')
    def groups_list(self, obj):
        return list(group for group in obj.groups.all())
    
    list_display = (
        "pk", "file", "families_list", "created_date",
        "groups_list", "tags_list"
        )
    search_fields = (
        "created_date","families",
        )
    list_filter = ("created_date", "families", "groups", "tags")
    empty_value_display = "-пусто-"
    inlines = [PhotoGroupAdmin,
               PhotoTagAdmin]
    exclude=("created_date",)
