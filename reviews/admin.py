from django.contrib import admin
from. models import Rating, Comment, Favourite
# Register your models here.


admin.site.register([Rating, Comment, Favourite])