from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blog-list"),
    path("post/<int:pk>/", BlogPostDetailView.as_view(), name="blog-detail"),
    path("post/create/", BlogPostCreateView.as_view(), name="blog-create"),
    path("post/<int:pk>/update/", BlogPostUpdateView.as_view(), name="blog-update"),
    path("post/<int:pk>/delete/", BlogPostDeleteView.as_view(), name="blog-delete"),
]