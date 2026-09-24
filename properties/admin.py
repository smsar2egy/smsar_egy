from django.contrib import admin
from .models import Property, PropertyImage, PropertyDate, Booking

# انلاين لعرض صور العقار الإضافية جوه صفحة العقار نفسها
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

# انلاين لعرض وتعديل تواريخ/أيام الحجز مباشرة من صفحة العقار
class PropertyDateInline(admin.TabularInline):
    model = PropertyDate
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'category', 'location', 'price', 'available', 'created_at')
    list_filter = ('property_type', 'category', 'location', 'available')
    search_fields = ('title', 'description', 'location')
    inlines = [PropertyImageInline, PropertyDateInline] # عشان تظهر الصور والتواريخ جوه العقار

@admin.register(PropertyDate)
class PropertyDateAdmin(admin.ModelAdmin):
    list_display = ('property', 'date', 'available')
    list_filter = ('available', 'date', 'property')
    search_fields = ('property__title',)
    list_editable = ('available',) # تتيح لك قفل أو فتح اليوم بضغطة زر مباشرة من جدول القائمة!

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'property', 'booking_date', 'booking_time', 'status', 'created_at')
    list_filter = ('status', 'booking_date', 'property')
    search_fields = ('full_name', 'phone', 'property__title')
    list_editable = ('status',) # تغيير حالة الحجز مباشرة من القائمة (تأكيد، ملغي، إلخ)