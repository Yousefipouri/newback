from django.urls import path

from . import views
from django.urls import path
from .views import DislikeCommentView, DislikePostView, LikeCommentView, LikePostView, PostCommentCreateView, PostCommentListView, PostCreateView, PostImageCreateView, PostImagesView, PostSearchAPIView, PostViewSet, UserPostDelete, UserPostList

# from .views import ToggleCommentLikeView


urlpatterns = [
    
    path('api/create-posts/', PostCreateView.as_view(), name='create-post'),

     path('api/create-posts/<int:post_id>/images/',
        PostImageCreateView.as_view(), name='post-image-create'),

    path('api/posts/<int:post_id>/images/', PostImagesView.as_view(), name='post-images'),

    path('api/posts/', UserPostList.as_view()),

    path('api/allposts/', PostViewSet.as_view()),

    path('api/deletepost/<int:pk>/', UserPostDelete.as_view()),

    path('api/post/<int:pk>/', views.PostRetrieve.as_view()),

    path('api/posts/<int:post_id>/comments/', PostCommentListView.as_view(), name='post-comment-list'),

    path('api/comments/create/', PostCommentCreateView.as_view(), name='post-comment-create'),

    path('api/searchposts/', PostSearchAPIView.as_view(), name='post-search'),

    path('api/cities/', views.get_cities),

    path('api/post/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    
    path('api/post/<int:post_id>/dislike/', DislikePostView.as_view(), name='dislike-post'),

    path('api/comment/<int:comment_id>/like/', LikeCommentView.as_view(), name='like-comment'),
    
    path('api/comment/<int:comment_id>/dislike/', DislikeCommentView.as_view(), name='dislike-comment'),

]
