from django.contrib import admin

from .models import Tag, Article


admin.site.register([Article, Tag])

# Register your models here.
