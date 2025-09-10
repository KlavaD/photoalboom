from django.shortcuts import render
from rest_framework import status, viewsets

from .serializers import (
    TagSerializer,
    GroupSerializer,
    PhotoSerializer,
    PostPhotoSerializer,
    FamilySerializer,
)
from photostorage.models import Tag, Group, Photo, Family


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    pagination_class = None
    serializer_class = GroupSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return PostPhotoSerializer
        return PhotoSerializer


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    pagination_class = None
    serializer_class = FamilySerializer
