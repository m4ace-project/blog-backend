from rest_framework import serializers
from blog.models import Post, Category, Comment, Reaction

class PostSerializer(serializers.ModelSerializer):
    
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
      model = Post
      fields = ['post_id', 'title', 'content', 'category', 'created_at', 'updated_at', 'is_published', 'published_at']


class CategorySerializer(serializers.ModelSerializer):
      
   class Meta:
      model = Category
      fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      fields = ['comment_id', 'post', 'author',  'content', 'created_at']
      read_only_fields = ['comment_id', 'post', 'author', 'created_at']


class ReactionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Reaction
      fields = ['id', 'user', 'post', 'reaction_type', 'created_at']
      ready_only_fields = ['id', 'user', 'post', 'created_at']


