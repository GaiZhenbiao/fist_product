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
    path('all_procedures', views.handle_get_all_procedures),
    path('upload', views.handle_upload),
    path('goto_stage', views.handle_goto_stage),
    path('set_as_approved', views.handle_set_as_approved),
    path('comment_procedure', views.handle_comment_procedure),
    path('is_commented', views.handle_is_commented),
    path('get_commented', views.handle_get_commented),
    path('finish_procedure', views.handle_finish_procedure),
    path('schedule_meeting', views.handle_schedule_meeting),
    path('add_news', views.handle_add_news),
    path('delete_news', views.handle_delete_news),
    path('cancel_fist', views.handle_cancel_fist),
    path('modify_graph', views.handle_modify_graph),
    path('delete_graph', views.handle_delete_graph),
    path('calculate_grade', views.handle_calculate_grade),
]
