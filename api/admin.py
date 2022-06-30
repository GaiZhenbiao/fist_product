from django.contrib import admin

from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ProcedureAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class UserUploadAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class GraphAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FistProcedure, ProcedureAdmin)
admin.site.register(UserUploadedFile, UserUploadAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Graph, GraphAdmin)
