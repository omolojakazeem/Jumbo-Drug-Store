from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    template = 'account/index.html'
    context = {
        "message": 'come and login',

    }
    return render(request, template_name=template, context=context)


@login_required
def dashboard(request):
    template = 'store/dashboard.html'
    context = {

    }
    return render(request, template_name=template, context=context)
