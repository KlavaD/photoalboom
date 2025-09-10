from django.urls import include, path
from rest_framework import routers

from .views import GroupViewSet, PhotoViewSet, TagViewSet


app_name = "api"

router = routers.DefaultRouter()
router.register("groups", GroupViewSet, basename="groups")
router.register("tags", TagViewSet, basename="tags")
router.register("photos", PhotoViewSet, basename="photos")

urlpatterns = [path("", include(router.urls))]
