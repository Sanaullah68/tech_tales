from rest_framework import routers
from .viewsets import BlogViewSets
router = routers.DefaultRouter()
router.register(r'blog', BlogViewSets)