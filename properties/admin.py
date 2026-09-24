from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Property,
    PropertyImage,
    PropertyDate,
    Booking,
)


# =========================
# PROPERTY IMAGES
# =========================

class PropertyImageInline(admin.TabularInline):

    model = PropertyImage

    extra = 1


# =========================
# PROPERTY DATES
# =========================

class PropertyDateInline(admin.TabularInline):

    model = PropertyDate

    extra = 1


# =========================
# PROPERTY ADMIN
# =========================

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'property_type',
        'category',
        'location',
        'price',
        'available',
        'calendar_button',
        'created_at',
    )

    list_filter = (
        'property_type',
        'category',
        'location',
        'available',
    )

    search_fields = (
        'title',
        'description',
        'location',
    )

    inlines = [
        PropertyImageInline,
        PropertyDateInline,
    ]

    def calendar_button(self, obj):

        url = reverse(
            'admin_calendar',
            args=[obj.id]
        )

        return format_html(
            '<a href="{}" '
            'style="background:#f5c518;'
            'color:#111;'
            'padding:6px 12px;'
            'border-radius:6px;'
            'text-decoration:none;'
            'font-weight:bold;">'
            '📅 إدارة المواعيد'
            '</a>',
            url
        )

    calendar_button.short_description = 'المواعيد'


# =========================
# PROPERTY DATE ADMIN
# =========================

@admin.register(PropertyDate)
class PropertyDateAdmin(admin.ModelAdmin):

    list_display = (
        'property',
        'date',
        'available',
    )

    list_filter = (
        'available',
        'date',
        'property',
    )

    search_fields = (
        'property__title',
    )

    list_editable = (
        'available',
    )


# =========================
# BOOKING ADMIN
# =========================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'property',
        'booking_date',
        'booking_time',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'booking_date',
        'property',
    )

    search_fields = (
        'full_name',
        'phone',
        'property__title',
    )

    list_editable = (
        'status',
    )