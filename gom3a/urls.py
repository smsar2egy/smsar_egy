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
    admin_calendar,
    admin_calendar_update,
)


urlpatterns = [

    # =========================
    # DJANGO ADMIN
    # =========================

    path(
        'admin/',
        admin.site.urls
    ),

    # =========================
    # HOME
    # =========================

    path(
        '',
        home,
        name='home'
    ),

    # =========================
    # PROPERTIES
    # =========================

    path(
        'properties/',
        property_list,
        name='property_list'
    ),

    # =========================
    # SALE
    # =========================

    path(
        'sale/',
        sale_properties,
        name='sale'
    ),

    # =========================
    # RENT
    # =========================

    path(
        'rent/',
        rent_properties,
        name='rent'
    ),

    # =========================
    # PROPERTY DETAIL
    # =========================

    path(
        'property/<int:pk>/',
        property_detail,
        name='property_detail'
    ),

    # =========================
    # BOOKING
    # =========================

    path(
        'booking/<int:pk>/',
        booking,
        name='booking'
    ),

    # =========================
    # ADMIN CALENDAR
    # =========================

    path(
        'admin/calendar/<int:property_id>/',
        admin_calendar,
        name='admin_calendar'
    ),

    path(
        'admin/calendar/<int:property_id>/update/',
        admin_calendar_update,
        name='admin_calendar_update'
    ),
]


# =========================
# MEDIA
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )