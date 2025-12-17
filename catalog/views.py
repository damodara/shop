from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "product_list.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо за сообщение, {name}!")
    return render(request, "contacts.html")
