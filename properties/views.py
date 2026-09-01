from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import Property, Booking, PropertyDate


# =========================
# HOME
# =========================

def home(request):

    properties = Property.objects.filter(
        available=True
    ).order_by('-created_at')

    for property in properties:

        if property.image:
            property.image_url = property.image.url
        else:
            property.image_url = ''

    return render(
        request,
        'home.html',
        {
            'properties': properties,
        }
    )


# =========================
# PROPERTY SEARCH / LIST
# =========================

def property_list(request):

    properties = Property.objects.filter(
        available=True
    ).order_by('-created_at')


    # =========================
    # SEARCH VALUES
    # =========================

    property_type = request.GET.get('type')
    category = request.GET.get('category')
    location = request.GET.get('location')


    # =========================
    # FILTER BY SALE / RENT
    # =========================

    if property_type in ['sale', 'rent']:

        properties = properties.filter(
            property_type=property_type
        )


    # =========================
    # FILTER BY CATEGORY
    # =========================

    valid_categories = [
        'apartment',
        'villa',
        'chalet',
        'summer',
        'property',
    ]

    if category in valid_categories:

        properties = properties.filter(
            category=category
        )


    # =========================
    # FILTER BY LOCATION
    # =========================

    valid_locations = [
        'cairo',
        'giza',
        'north_coast',
        'hurghada',
        'dahab',
        'sharm',
        'ain_sokhna',
    ]

    if location in valid_locations:

        properties = properties.filter(
            location=location
        )


    # =========================
    # PAGE
    # =========================

    return render(
        request,
        'properties.html',
        {
            'properties': properties,

            'selected_type': property_type,

            'selected_category': category,

            'selected_location': location,
        }
    )


# =========================
# SALE
# =========================

def sale_properties(request):

    properties = Property.objects.filter(
        available=True,
        property_type='sale'
    ).order_by('-created_at')

    return render(
        request,
        'sale.html',
        {
            'properties': properties,
        }
    )


# =========================
# RENT
# =========================

def rent_properties(request):

    properties = Property.objects.filter(
        available=True,
        property_type='rent'
    ).order_by('-created_at')

    return render(
        request,
        'rent.html',
        {
            'properties': properties,
        }
    )


# =========================
# PROPERTY DETAIL
# =========================

def property_detail(request, pk):

    property = get_object_or_404(
        Property,
        pk=pk
    )

    dates = property.dates.all()

    return render(
        request,
        'property_detail.html',
        {
            'property': property,
            'dates': dates,
        }
    )


# =========================
# BOOKING
# =========================

def booking(request, pk):

    property = get_object_or_404(
        Property,
        pk=pk,
        available=True
    )

    selected_date = request.GET.get('date')

    if request.method == 'POST':

        full_name = request.POST.get(
            'full_name',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        guests_count = request.POST.get(
            'guests_count'
        )

        booking_date = request.POST.get(
            'booking_date'
        )

        booking_time = request.POST.get(
            'booking_time'
        )

        id_card = request.FILES.get(
            'id_card'
        )


        # =========================
        # CHECK REQUIRED DATA
        # =========================

        if not all([
            full_name,
            phone,
            guests_count,
            booking_date,
            booking_time,
            id_card
        ]):

            messages.error(
                request,
                'من فضلك املأ كل البيانات المطلوبة.'
            )


        else:

            # =========================
            # CHECK BLOCKED DATE
            # =========================

            blocked_date = PropertyDate.objects.filter(
                property=property,
                date=booking_date,
                available=False
            ).exists()


            if blocked_date:

                messages.error(
                    request,
                    'اليوم ده غير متاح للحجز.'
                )


            else:

                # =========================
                # CREATE BOOKING
                # =========================

                Booking.objects.create(

                    property=property,

                    full_name=full_name,

                    phone=phone,

                    guests_count=guests_count,

                    id_card=id_card,

                    booking_date=booking_date,

                    booking_time=booking_time,

                )


                # =========================
                # SUCCESS PAGE
                # =========================

                return render(
                    request,
                    'booking_success.html',
                    {
                        'property': property,
                        'booking_date': booking_date,
                        'booking_time': booking_time,
                    }
                )


    # =========================
    # BOOKING PAGE
    # =========================

    return render(
        request,
        'booking.html',
        {
            'property': property,
            'selected_date': selected_date,
        }
    )