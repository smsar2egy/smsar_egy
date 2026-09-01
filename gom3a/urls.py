from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from properties.views import (
    home,
    property_list,
    property_detail,
    sale_properties,
    rent_properties,
    booking,
)


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'properties/',
        property_list,
        name='property_list'
    ),

    path(
        'sale/',
        sale_properties,
        name='sale'
    ),

    path(
        'rent/',
        rent_properties,
        name='rent'
    ),

    path(
        'property/<int:pk>/',
        property_detail,
        name='property_detail'
    ),

    path(
        'booking/<int:pk>/',
        booking,
        name='booking'
    ),
]


# تشغيل صور الـ MEDIA أثناء التطوير
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )