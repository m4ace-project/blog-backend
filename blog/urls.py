from django.urls import path
from . import views
from .views import CategoryList, EditCommentView, DeleteCommentView, PostCommentsListView, LikePostView, UnLikePostView, ViewPosts, TopAuthorsByCategoryView, AddFavouriteAuthorView




urlpatterns = [
    path('postview/', ViewPosts.as_view(), name='viewposts'),
    path('posts/', views.PostList.as_view(), name='all_posts'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name='specific_post'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:category_id>/top-authors/', TopAuthorsByCategoryView.as_view(), name='top-authors-by-category'),
    path('posts/<int:post_id>/comments/', views.CreateCommentView.as_view(), name='create_comment'),
    path('comments/<int:pk>/edit/', EditCommentView.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
    path('posts/<int:post_id>/commentslist/', PostCommentsListView.as_view(), name='post_comments_list'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/unlike/', UnLikePostView.as_view(), name='unlike-post'),
    path('add-favourite-author/', AddFavouriteAuthorView.as_view(), name='add-favourite-author'),   
]