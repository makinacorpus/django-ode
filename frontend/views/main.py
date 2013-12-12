from django.shortcuts import render

from accounts.models import Organization


def home(request):
    context = {}
    providers = Organization.objects\
        .filter(is_provider=True).exclude(picture='').order_by('?')[:18]
    consumers = Organization.objects\
        .filter(is_consumer=True).exclude(picture='').order_by('?')[:18]
    context['providers'] = list(providers)
    context['consumers'] = list(consumers)
    context['providers_range'] = range(len(providers))
    context['consumers_range'] = range(len(consumers))
    return render(request, 'home.html', context)
