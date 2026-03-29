from rest_framework import generics, permissions
from .models import News
from .serializers import NewsSerializer

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Allows GET (list) for everyone, but POST (create) only for superusers.
    """
    def has_permission(self, request, view):
        # Allow read-only methods for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is a superuser for POST requests
        return bool(request.user and request.user.is_superuser)

class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by("-created_at")
    serializer_class = NewsSerializer
    permission_classes = [IsSuperUserOrReadOnly]
