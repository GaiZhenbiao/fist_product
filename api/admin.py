from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(FistProcedure)
admin.site.register(UserUploadedFile)
admin.site.register(Comment)