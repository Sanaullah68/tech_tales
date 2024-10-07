from rest_framework import viewsets
from .serializer import BlogSerializer,Blog
class BlogViewSets(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer