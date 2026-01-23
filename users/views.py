from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.form import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("user:login")