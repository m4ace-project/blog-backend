from rest_framework import serializers
from blog.models import Post, Category, Comment, Like, ReaderCategory
from userProfile.models import ContentCreatorProfile


class PostSerializer(serializers.ModelSerializer):
    
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
      model = Post
      fields = ['post_id', 'title', 'content', 'category', 'created_at', 'updated_at', 'is_published', 'published_at']

class PostListSerializer(serializers.ModelSerializer):
   preview = serializers.SerializerMethodField()

   class Meta:
      model = Post
      fields = ['post_id', 'title', 'preview', 'category', 'created_at', 'updated_at', 'is_published', 'published_at']

   def get_preview(self, obj):
      return obj.content[:200] + ('...' if len(obj.content) > 200 else '')
   

class CategorySerializer(serializers.ModelSerializer):
      
   class Meta:
      model = Category
      fields = ['id', 'name']

class TopAuthorSerializer(serializers.Serializer):
   author_id = serializers.IntegerField(source='post__author')
   author_name = serializers.CharField(source='post__author__contentcreatorprofile__name')
   total_likes = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      fields = ['comment_id', 'post', 'author',  'content', 'created_at']
      read_only_fields = ['comment_id', 'post', 'author', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
   class Meta:
      model = Like
      fields = ['id', 'user', 'post', 'created_at']
      read_only_fields = ['id', 'user', 'created_at']


class ReaderCategorySerializer(serializers.ModelSerializer):
   reader_id = serializers.IntegerField(source='reader.id', read_only=True)
   category_name = serializers.CharField(source='category.name', read_only=True)
   author_name = serializers.CharField(source='author.name', read_only=True)

   class Meta:
      model = ReaderCategory
      fields = ['reader_id', 'category_name', 'author_name']

      