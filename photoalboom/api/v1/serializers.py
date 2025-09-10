from rest_framework import serializers

from photostorage.models import Group, Tag, Family, Photo


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title", "slug")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ("id", "title", "slug", "creator", "members")


class PhotoSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(
        many=True,
    )
    tags = serializers.StringRelatedField(
        many=True,
    )
    families = serializers.StringRelatedField(
        many=True,
    )
    created_date = serializers.DateField()
    uploaded_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Photo
        fields = (
            "id",
            "file",
            "families",
            "created_date",
            "groups",
            "tags",
            "uploaded_at",
            "uploaded_by",
        )


class PostPhotoSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(), slug_field="id", many=True
    )
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(), slug_field="id", many=True
    )

    class Meta:
        model = Photo
        fields = (
            "id",
            "file",
            "families",
            "groups",
            "tags",
        )

    def create(self, validated_data):
        families = validated_data.pop("families")
        groups = validated_data.pop("groups")
        tags = validated_data.pop("tags")
        photo = Photo.objects.create(
            **validated_data, uploaded_by=self.context["request"].user
        )
        photo.families.set(families)
        photo.groups.set(groups)
        photo.tags.set(tags)
        return photo

    def to_representation(self, instance):
        return PhotoSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
