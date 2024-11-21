from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from rest_framework import permissions, status, generics 
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, PostComment,PostImage
from .serializers import PostCommentSerializer, PostCreateSerializer, PostSerializer, PostWithImagesSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostImageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination 
import csv
import os
from django.http import JsonResponse


class PostPagination(PageNumberPagination): 
    page_size = 6 # Number of posts per page 
    page_size_query_param = 'page_size' 
    max_page_size = 100

class PostViewSet(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    def get_queryset(self):
        queryset = Post.objects.filter(approved=True)
        
        # دریافت پارامترهای فیلتر از درخواست
        is_nature = self.request.query_params.get('isNature', None)
        is_religious = self.request.query_params.get('isReligious', None)
        is_historical = self.request.query_params.get('isHistorical', None)
        is_indoor = self.request.query_params.get('isIndoor', None)
        city = self.request.query_params.get('city', None)
        sort_by = self.request.query_params.get('sort', None)


        # اعمال فیلترها فقط اگر مقدار آن‌ها true باشد
        filters = Q()
        if is_nature == 'true':
            filters &= Q(isNature=True)
        if is_religious == 'true':
            filters &= Q(isReligious=True)
        if is_historical == 'true':
            filters &= Q(isHistorical=True)
        if is_indoor == 'true':
            filters &= Q(isIndoor=True)
        if city:
            filters &= Q(city__icontains=city)

        queryset = queryset.filter(filters)

        if sort_by == 'time':
             queryset = queryset.order_by('-created_at')
        elif sort_by == 'likes':
             queryset = queryset.annotate(
                    like_dislike_diff=Count('likes') - Count('dislikes') ).order_by('-like_dislike_diff')
        else:
            queryset = queryset.order_by('id')
        return queryset
  
class PostImageCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)
        images = request.FILES.getlist('image')
        
        for image in images:
            PostImage.objects.create(post=post, image=image)
        
        return Response(data='تصاویر با موفقیت آپلود شدند', status=status.HTTP_201_CREATED)

class PostImagesView(generics.ListAPIView):
    serializer_class = PostImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return PostImage.objects.filter(post_id=post_id)
    
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPostList(generics.ListCreateAPIView):
    serializer_class = PostWithImagesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
class UserPostDelete(generics.DestroyAPIView):
    serializer_class = PostWithImagesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data='حذف با موفقیت انجام شد', status=status.HTTP_202_ACCEPTED)

class PostCommentCreateView(generics.CreateAPIView):
     queryset = PostComment.objects.all() 
     serializer_class = PostCommentSerializer 
     permission_classes = [permissions.IsAuthenticated] 

     def perform_create(self, serializer): 
         serializer.save(user=self.request.user)

class PostCommentListView(generics.ListAPIView):
     serializer_class = PostCommentSerializer 
     def get_queryset(self): 
        post_id = self.kwargs['post_id'] 
        return PostComment.objects.filter(post_id=post_id)
     


class PostRetrieve(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class PostSearchAPIView(generics.ListAPIView):
     serializer_class = PostSerializer
     def get_queryset(self):
         query = self.request.query_params.get('q', None)
         if query:
             return Post.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(user__username__icontains=query),
                                      approved=True  )
         return Post.objects.filter(approved=True)
     

class LikePostView(APIView):
      permission_classes = [permissions.IsAuthenticated]
      def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        if user in post.likes.all():
            post.likes.remove(user)
            message = "Unliked"
        else:
            post.likes.add(user)
            post.dislikes.remove(user)
            message = "Liked"

        return Response({'msg': message}, status=status.HTTP_200_OK)

class DislikePostView(APIView):
       permission_classes = [permissions.IsAuthenticated]
       def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        if user in post.dislikes.all():
            post.dislikes.remove(user)
            message = "Undisliked"
        else:
            post.dislikes.add(user)
            post.likes.remove(user)
            message = "Disliked"

        return Response({'msg': message}, status=status.HTTP_200_OK)

class LikeCommentView(APIView):
      permission_classes = [permissions.IsAuthenticated]
      def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(PostComment, id=comment_id)
        user = request.user
        
        if user in comment.likes.all():
            comment.likes.remove(user)
            message = "Unliked"
        else:
            comment.likes.add(user)
            comment.dislikes.remove(user)
            message = "Liked"

        return Response({'msg': message}, status=status.HTTP_200_OK)

class DislikeCommentView(APIView):
       permission_classes = [permissions.IsAuthenticated]
       def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(PostComment, id=comment_id)
        user = request.user
        
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
            message = "Undisliked"
        else:
            comment.dislikes.add(user)
            comment.likes.remove(user)
            message = "Disliked"

        return Response({'msg': message}, status=status.HTTP_200_OK)
       

def get_cities(request):
    cities = []
    current_file_path = os.path.dirname(__file__)
    csv_file_path = os.path.abspath(os.path.join(current_file_path, '..', 'shahr.csv'))  # Adjust the path as needed

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cities.append(row['name'])  # Read the 'name' column for city names

    return JsonResponse(cities, safe=False)