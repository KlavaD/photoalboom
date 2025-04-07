from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from pytils.translit import slugify

class Family(models.Model):
    title = models.CharField("Фамилия", max_length=200)
    slug = models.CharField(unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Семья'
        verbose_name_plural = 'Семьи'

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
class Group(models.Model):
    title = models.CharField("Название группы фотографий", max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField("Описание группы",blank=True, null=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField("Название тэга", max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Photo(models.Model):
    image = models.ImageField(
        'Фото',
        upload_to='photo/',
        blank=True
    )
    family = models.ForeignKey(
        Family,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Семья"

    )
    created_date = models.DateTimeField(
        'Дата фотографии',
    )
    
    group = models.ManyToManyField(
        Group,
        blank=True,
        through="PhotoGroup",
        verbose_name="Группы"
    )

    tag = models.ManyToManyField(
        Tag,
        blank=True,
        through="PhotoTag",
        verbose_name="Тэги"
    )
    
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        default_related_name = 'photo'


class PhotoGroup(models.Model):
    group = models.ForeignKey(
        Group,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото:Группа'
        verbose_name_plural = 'Фото:Группы'

    def __str__(self):
        return f'{self.group} {self.photo}'
    
class PhotoTag(models.Model):
    tags = models.ForeignKey(
        Tag,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото:Тэг'
        verbose_name_plural = 'Фото:Тэги'

    def __str__(self):
        return f'{self.tags} {self.photo}'
    