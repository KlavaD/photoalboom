from django.shortcuts import render

from .models import Photo


def index(request):
    image_list = Photo.objects.all().prefetch_related(
        "families", "tags", "groups"
    )
    context = {
        "page_obj": image_list,
    }
    return render(request, "images/index.html", context)
