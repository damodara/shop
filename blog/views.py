from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Показываем только опубликованные записи"""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличиваем счётчик просмотров при открытии статьи"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])
        return obj


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    template_name = "blog/blog_form.html"
    fields = ("title", "content", "preview", "is_published")
    success_url = reverse_lazy("blog:blog-list")
    permission_required = "blog.add_blogpost"

    def has_permission(self):
        """Проверяем, что пользователь в группе Контент-менеджер"""
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.groups.filter(name="Контент-менеджер").exists()


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    template_name = "blog/blog_form.html"
    fields = ("title", "content", "preview", "is_published")
    permission_required = "blog.change_blogpost"

    def has_permission(self):
        """Проверяем, что пользователь в группе Контент-менеджер"""
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.groups.filter(name="Контент-менеджер").exists()

    def get_success_url(self):
        """После редактирования — редирект на просмотр статьи"""
        return reverse("blog:blog-detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog-list")
    permission_required = "blog.delete_blogpost"

    def has_permission(self):
        """Проверяем, что пользователь в группе Контент-менеджер"""
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.groups.filter(name="Контент-менеджер").exists()