from django.shortcuts import render

from zinnia.managers import PUBLISHED
from zinnia.models.entry import Entry

from accounts.models import Organization

from ..models import CarouselImage

def home(request):
    context = {}

    blog_entries = Entry.objects.filter(status=PUBLISHED)[:2]
    context['blog_entries'] = list(blog_entries)

    providers = Organization.objects\
        .filter(is_provider=True).exclude(picture='').order_by('?')[:18]
    consumers = Organization.objects\
        .filter(is_consumer=True).exclude(picture='').order_by('?')[:18]
    context['providers'] = list(providers)
    context['consumers'] = list(consumers)
    context['providers_range'] = range(len(providers))
    context['consumers_range'] = range(len(consumers))

    context['carousel_images'] = CarouselImage.objects.all()

    return render(request, 'home.html', context)
