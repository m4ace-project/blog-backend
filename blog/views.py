from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Post, Category, Comment, Like, ReaderCategory, ContentCreatorProfile
from blog.serializers import PostSerializer, PostListSerializer, CategorySerializer, CommentSerializer, TopAuthorSerializer, ReaderCategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404


# View to see first 200 characters of a blog post
class ViewPosts(APIView):
    def get(self, request):
        posts = Post.objects.filter(is_published= True)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostList(APIView):
    permission_classes = [IsAuthenticated]
# List all the available post, or creates a new post
    def get(self, request):

        # Check if the user is a reader and filter posts accordingly.
        if request.user.role == 'reader':
            posts = Post.objects.filter(is_published=True)

        else:
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # To create new blog post      
    def post(self, request):
        if request.user.role != 'content_creator':
            return Response({'error': 'You do not have the permission to create posts.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update or de;ete a particular post.

class PostDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
           return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk):
        if request.user.role != 'content_creator':
            return Response({"error": "You do not have permission to edit posts."}, status=status.HTTP_403_FORBIDDEN)

        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        if request.user.role != 'content_creator':
            return Response({"error": "You do not have permission to delete posts."}, status=status.HTTP_403_FORBIDDEN)

        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

    
class CategoryList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_top_authors_by_likes(category_id):
    top_authors = (
        Like.objects.filter(post__category_id=category_id)
        .values('post__author', 'post__author__contentcreatorprofile__name') # Group by author and get name
        .annotate(total_likes=Count('id'))  # Count Likes
        .order_by('-total_likes')[:5]   # Sort by likes and limit to top 5

    )
    return top_authors

class TopAuthorsByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get top authors by likes
        top_authors = get_top_authors_by_likes(category_id)
        serializer = TopAuthorSerializer(top_authors, many=True)
        return Response(serializer.data)
    

class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(post_id=post_id)
        serializer.save(post=post, author=self.request.user)

class EditCommentView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = super().get_object()

        if comment.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this comment.")
        return comment

        

class DeleteCommentView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = super().get_object()

        if comment.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        return comment
    
class PostCommentsListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')
    
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.filter(post_id=post_id).first()
        if not post:
            return Response({"error":"Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        return Response({"message": "You have already liked this post."}, status=status.HTTP_200_OK)

class UnLikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        post = Post.objects.filter(post_id=post_id).first()
        if not post:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "Like removed successfully."}, status=status.HTTP_200_OK)
        
        return Response({"message": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
    

class AddFavouriteAuthorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reader = request.user
        data = request.data

        if not isinstance(data, list):
            return Response({
                "detail": "Input data must be a list of objects with 'category_id' and 'author_id'."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        created_entries = []
        errors = []

        for entry in data:
            category_id = entry.get('category_id')
            author_id = entry.get('author_id')

            # Validate category_id and author_id
            if not category_id or not author_id:
                errors.append({
                    "category_id": category_id,
                    "author_id": author_id,
                    "detail": "Both category_id and author_id are required."
                })

                continue

            # Fetch category and author
            try:
                category = Category.objects.get(id=category_id)
                author = ContentCreatorProfile.objects.get(profile_id=author_id)
            except (Category.DoesNotExist, ContentCreatorProfile.DoesNotExist):
                errors.append({
                    "category_id": category_id,
                    "author_id": author_id,
                    "detail": "Invalid category_id or author_id."
                })
                continue

            # Check if the favourite author already exists
            if ReaderCategory.objects.filter(reader=reader, category=category, author=author).exists():
                errors.append({
                    "category_id": category_id,
                    "author_id": author_id,
                    "detail": "This author is already a favourite for the selected category."
                })

                continue

            # Create a new ReaderCategory entry
            reader_category = ReaderCategory.objects.create(
                reader=reader, category=category, author=author
            )
            created_entries.append(reader_category)
        
        # Serialize created entries
        serializer = ReaderCategorySerializer(created_entries, many=True)
        return Response({
            "created": serializer.data,
            "errors": errors
        }, status=status.HTTP_201_CREATED if created_entries else status.HTTP_400_BAD_REQUEST)
    