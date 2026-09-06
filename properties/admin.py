from django.contrib import admin
from .models import Property, PropertyImage, PropertyDate, Booking


# =========================
# PROPERTY IMAGES INLINE
# =========================

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 5
    fields = ('image', 'order')


# =========================
# PROPERTY DATES INLINE
# =========================

class PropertyDateInline(admin.TabularInline):
    model = PropertyDate
    extra = 3


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
    )

    inlines = [
        PropertyImageInline,
        PropertyDateInline,
    ]


# =========================
# PROPERTY IMAGE ADMIN
# =========================

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):

    list_display = (
        'property',
        'order',
        'created_at',
    )


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
    )


# =========================
# BOOKING ADMIN
# =========================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'property',
        'phone',
        'booking_date',
        'booking_time',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'booking_date',
    )

    search_fields = (
        'full_name',
        'phone',
    )