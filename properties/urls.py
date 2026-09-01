from django.urls import path

from .views import (
    home,
    property_list,
    property_detail,
    sale_properties,
    rent_properties,
    booking,
)


urlpatterns = [

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

]