from datetime import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

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

    property_type = request.GET.get('type')
    category = request.GET.get('category')
    location = request.GET.get('location')

    # SALE / RENT

    if property_type in ['sale', 'rent']:

        properties = properties.filter(
            property_type=property_type
        )

    # CATEGORY

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

    # LOCATION

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

        # CHECK REQUIRED DATA

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

            # CHECK BLOCKED DATE

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

                # CREATE BOOKING

                Booking.objects.create(
                    property=property,
                    full_name=full_name,
                    phone=phone,
                    guests_count=guests_count,
                    id_card=id_card,
                    booking_date=booking_date,
                    booking_time=booking_time,
                )

                return render(
                    request,
                    'booking_success.html',
                    {
                        'property': property,
                        'booking_date': booking_date,
                        'booking_time': booking_time,
                    }
                )

    return render(
        request,
        'booking.html',
        {
            'property': property,
            'selected_date': selected_date,
        }
    )


# =========================
# ADMIN CALENDAR
# =========================

def admin_calendar(request, property_id):

    property = get_object_or_404(
        Property,
        id=property_id
    )

    dates = property.dates.all()

    return render(
        request,
        'admin/property_calender.html',
        {
            'property': property,
            'dates': dates,
        }
    )


# =========================
# ADMIN CALENDAR UPDATE
# =========================

@require_POST
def admin_calendar_update(request, property_id):

    property = get_object_or_404(
        Property,
        id=property_id
    )

    date_string = request.POST.get('date')
    status = request.POST.get('status')

    if not date_string or status not in [
        'available',
        'booked'
    ]:

        return JsonResponse(
            {
                'success': False,
                'error': 'بيانات غير صحيحة'
            },
            status=400
        )

    try:

        selected_date = datetime.strptime(
            date_string,
            '%Y-%m-%d'
        ).date()

    except ValueError:

        return JsonResponse(
            {
                'success': False,
                'error': 'التاريخ غير صحيح'
            },
            status=400
        )

    property_date, created = PropertyDate.objects.get_or_create(
        property=property,
        date=selected_date
    )

    property_date.available = (
        status == 'available'
    )

    property_date.save()

    return JsonResponse(
        {
            'success': True,
            'available': property_date.available
        }
    )