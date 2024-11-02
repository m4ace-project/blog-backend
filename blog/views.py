from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Post, Category, Comment, Reaction
from blog.serializers import PostSerializer, CategorySerializer, CommentSerializer, ReactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


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
    

class ReactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(post_id=post_id)
        reaction_type = request.data.get('reaction_type')

        # Get or create the reaction for the user and post
        reaction, created = Reaction.objects.get_or_create(
            user = request.user, post=post,
            defaults={'reaction_type': reaction_type}
        )

        if not created:
            # Update reaction type if it exists
            reaction.reaction_type = reaction_type
            reaction.save()

        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def deltete(self, request, post_id):
        # Remove a user's reaction from a post               
        try:
            post = Post.objects.get(post_id=post_id)
            reaction = Reaction.objects.get(user=request.user, post=post)
            reaction.delete()
            return Response({"message": "Reaction deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Reaction.DoesNotExist:
            return Response({'error': 'Reaction not found.'}, status=status.HTTP_404_NOT_FOUND)
        
