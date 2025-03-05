from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    path(
        '',
        views.chatListView.as_view(),
        name='chat_list'
    ),
    path(
        'tag/<slug:tag_slug>/',
        views.chatListView.as_view(),
        name='chat_list_by_tag'
    ),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:chat>/',
        views.chat_detail,
        name='chat_detail'
    ),
    path(
        '<int:chat_id>/comment/',
        views.chat_comment,
        name='chat_comment'
    ),

    path(
        'comment/<int:comment_id>/edit/',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        'comment/<int:comment_id>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),
]