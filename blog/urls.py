from django.urls import path
from . import views
from .views import CategoryList, EditCommentView, DeleteCommentView, PostCommentsListView, ReactionView




urlpatterns = [
    path('posts/', views.PostList.as_view(), name='all_posts'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name='specific_post'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('posts/<int:post_id>/comments/', views.CreateCommentView.as_view(), name='create_comment'),
    path('comments/<int:pk>/edit/', EditCommentView.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
    path('posts/<int:post_id>/commentslist/', PostCommentsListView.as_view(), name='post_comments_list'),
    path('posts/<int:post_id>/reaction/', ReactionView.as_view(), name='post-reaction'),
]