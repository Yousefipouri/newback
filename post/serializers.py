from rest_framework import serializers
from account.models import MyUser
from .models import Post, PostComment, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id','image']

class PostCommentSerializer(serializers.ModelSerializer): 
    user = serializers.ReadOnlyField(source='user.username') 
    number_of_likes = serializers.ReadOnlyField()
    number_of_dislikes = serializers.ReadOnlyField()
    class Meta: 
        model = PostComment 
        fields = ['id', 'user', 'post', 'body','created_at','number_of_dislikes','number_of_likes']

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    comments = PostCommentSerializer(many=True, read_only=True)
    number_of_likes = serializers.ReadOnlyField()
    number_of_dislikes = serializers.ReadOnlyField()
    comment_count = serializers.SerializerMethodField()  # تعداد نظرات

    class Meta:
        model = Post
        fields = ['id', 'title', 'city','created_at', 'description', 'address', 'latitude', 'longitude', 'isReligious', 'isNature', 'isIndoor', 'isHistorical', 'images', 'user', 'comments', 'number_of_dislikes','number_of_likes', 'comment_count', 'approved']

    def get_comment_count(self, obj):
        return PostComment.objects.filter(post=obj).count()  # تعداد نظرات
    
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'city', 'description', 'address', 'latitude', 'longitude', 'isReligious', 'isNature', 'isIndoor','isHistorical']

class PostWithImagesSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'city', 'description', 'address', 'latitude', 'longitude', 'isReligious', 'isNature', 'isIndoor', 'isHistorical', 'images','approved']
        read_only_fields = ['approved']




