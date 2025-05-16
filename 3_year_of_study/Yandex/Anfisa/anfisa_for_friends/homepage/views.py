# homepage/views.py
from django.shortcuts import render
from ice_cream.models import IceCream


def index(request):
    template_name = 'homepage/index.html'

    ice_cream_list = IceCream.objects.all()

    context = {
        'ice_cream_list': ice_cream_list,
    }
    return render(request, template_name, context)