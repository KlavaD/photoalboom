from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify
from PIL import Image
from PIL.ExifTags import TAGS
from django.utils.timezone import make_aware
import datetime

User = get_user_model()


class SlugAbs(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Family(SlugAbs):
    title = models.CharField("Фамилия", max_length=200)
    slug = models.CharField(unique=True, max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        User, through="FamilyMember", related_name="families"
    )

    class Meta:
        verbose_name = "Семья"
        verbose_name_plural = "Семьи"

    def __str__(self) -> str:
        return self.title


class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)


class Group(SlugAbs):
    title = models.CharField("Название группы фотографий", max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField("Описание группы", blank=True, null=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return self.title


class Tag(SlugAbs):
    title = models.CharField("Название тэга", max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self) -> str:
        return self.title


class Photo(models.Model):
    file = models.ImageField("Фото", upload_to="photos/", blank=True)
    families = models.ManyToManyField(
        Family, blank=False, null=False, verbose_name="Семья"
    )
    created_date = models.DateField(
        "Дата фотографии",
    )

    groups = models.ManyToManyField(
        Group, blank=True, through="PhotoGroup", verbose_name="Группы"
    )

    tags = models.ManyToManyField(
        Tag, blank=True, through="PhotoTag", verbose_name="Тэги"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_photos"
    )

    def save(self, *args, **kwargs):
        # Если дата съёмки ещё не установлена — пробуем извлечь из EXIF
        if not self.created_date and self.file:
            try:
                image = Image.open(self.file)
                exif_data = image._getexif()
                if exif_data:
                    for tag, value in exif_data.items():
                        tag_name = TAGS.get(tag)
                        if (
                            tag_name == "DateTimeOriginal"
                            or tag_name == "DateTime"
                        ):
                            # Очищаем строку от лишних символов и нулевых байтов
                            cleaned_value = value.strip().rstrip("\x00")

                            # Пробуем разные форматы даты
                            try:
                                dt = datetime.datetime.strptime(
                                    cleaned_value, "%Y:%m:%d %H:%M:%S"
                                )
                            except ValueError:
                                # Пробуем альтернативный формат
                                try:
                                    dt = datetime.datetime.strptime(
                                        cleaned_value, "%Y-%m-%d %H:%M:%S"
                                    )
                                except ValueError:
                                    # Если не удается распарсить, пропускаем
                                    continue
                            self.created_date = dt.date()
                            break
            except Exception as e:
                # Можно залогировать или проигнорировать
                pass

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"
        default_related_name = "photos"
        ordering = ("-created_date",)


class PhotoGroup(models.Model):
    group = models.ForeignKey(
        Group, blank=False, null=False, on_delete=models.CASCADE
    )
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Фото:Группа"
        verbose_name_plural = "Фото:Группы"

    def __str__(self):
        return f"{self.group} {self.photo}"


class PhotoTag(models.Model):
    tags = models.ForeignKey(
        Tag, blank=False, null=False, on_delete=models.CASCADE
    )
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Фото:Тэг"
        verbose_name_plural = "Фото:Тэги"

    def __str__(self):
        return f"{self.tags} {self.photo}"
