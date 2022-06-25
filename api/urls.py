from django.urls import path

from . import views

urlpatterns = [
    path('login', views.handle_login),
    path('find_product', views.handle_find_product),
    path('modify_product', views.handle_modify_product),
    path('all_products', views.handle_get_all_products),
    path('delete_product', views.handle_delete_product),
    path('create_procecure', views.handle_create_procecure),
    path('like_procedure', views.handle_like_procedure),
    path('find_procedure', views.handle_find_procedure),
    path('upload', views.handle_upload),
    path('all_procedures', views.handle_get_all_procedures),
    path('goto_stage', views.handle_goto_stage),
    path('comment_procedure', views.handle_comment_procedure),
    path('finish_procedure', views.handle_finish_procedure),
]
