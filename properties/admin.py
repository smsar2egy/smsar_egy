from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import format_html
from django.contrib import messages
from datetime import date
import calendar

from .models import Property, PropertyDate, Booking


# =========================================================
# PROPERTY ADMIN
# =========================================================

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "property_type",
        "category",
        "location",
        "price",
        "available",
        "calendar_button",
        "created_at",
    )

    list_filter = (
        "property_type",
        "category",
        "location",
        "available",
    )

    search_fields = (
        "title",
        "location",
        "description",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    # =====================================================
    # لما ندوس على العقار نفتح صفحة التقويم
    # =====================================================

    def change_view(self, request, object_id, form_url="", extra_context=None):

        return redirect(
            "admin:property_calendar",
            object_id=object_id
        )

    # =====================================================
    # زر التقويم
    # =====================================================

    @admin.display(description="أيام الحجز")
    def calendar_button(self, obj):

        url = reverse(
            "admin:property_calendar",
            args=[obj.pk]
        )

        return format_html(
            '<a href="{}" '
            'style="'
            'background:#D4A72C;'
            'color:#000;'
            'padding:6px 12px;'
            'border-radius:5px;'
            'font-weight:bold;'
            'text-decoration:none;'
            '">'
            '📅 التقويم'
            '</a>',
            url
        )

    # =====================================================
    # CUSTOM URLS
    # =====================================================

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [

            path(
                "<int:object_id>/calendar/",
                self.admin_site.admin_view(
                    self.property_calendar
                ),
                name="property_calendar",
            ),

            path(
                "<int:object_id>/calendar/toggle/",
                self.admin_site.admin_view(
                    self.toggle_date
                ),
                name="property_calendar_toggle",
            ),

        ]

        return custom_urls + urls

    # =====================================================
    # CALENDAR PAGE
    # =====================================================

    def property_calendar(self, request, object_id):

        property_obj = get_object_or_404(
            Property,
            pk=object_id
        )

        # الشهر الحالي
        today = date.today()

        try:

            year = int(
                request.GET.get(
                    "year",
                    today.year
                )
            )

            month = int(
                request.GET.get(
                    "month",
                    today.month
                )
            )

            if month < 1:

                month = 12
                year -= 1

            elif month > 12:

                month = 1
                year += 1

        except (ValueError, TypeError):

            year = today.year
            month = today.month

        # =================================================
        # الشهر السابق
        # =================================================

        if month == 1:

            prev_year = year - 1
            prev_month = 12

        else:

            prev_year = year
            prev_month = month - 1

        # =================================================
        # الشهر التالي
        # =================================================

        if month == 12:

            next_year = year + 1
            next_month = 1

        else:

            next_year = year
            next_month = month + 1

        # =================================================
        # أسماء الشهور
        # =================================================

        months = [

            "يناير",
            "فبراير",
            "مارس",
            "أبريل",
            "مايو",
            "يونيو",
            "يوليو",
            "أغسطس",
            "سبتمبر",
            "أكتوبر",
            "نوفمبر",
            "ديسمبر",

        ]

        month_name = months[month - 1]

        # =================================================
        # أيام الأسبوع
        # =================================================

        weekdays = [

            "الاثنين",
            "الثلاثاء",
            "الأربعاء",
            "الخميس",
            "الجمعة",
            "السبت",
            "الأحد",

        ]

        # =================================================
        # عدد أيام الشهر
        # =================================================

        days_count = calendar.monthrange(
            year,
            month
        )[1]

        # =================================================
        # بيانات الأيام
        # =================================================

        days = []

        for day_number in range(
            1,
            days_count + 1
        ):

            current_day = date(
                year,
                month,
                day_number
            )

            property_date = PropertyDate.objects.filter(
                property=property_obj,
                date=current_day
            ).first()

            # لو اليوم مش موجود في قاعدة البيانات
            # نعتبره متاح
            if property_date:

                available = property_date.available

            else:

                available = True

            weekday = weekdays[
                current_day.weekday()
            ]

            days.append({

                "date": current_day,

                "date_text":
                    current_day.strftime(
                        "%d/%m/%Y"
                    ),

                "day_name":
                    weekday,

                "available":
                    available,

                "exists":
                    property_date is not None,

            })

        context = {

            **self.admin_site.each_context(request),

            "title":
                f"أيام الحجز - {property_obj.title}",

            "property":
                property_obj,

            "days":
                days,

            "month_name":
                month_name,

            "year":
                year,

            "prev_year":
                prev_year,

            "prev_month":
                prev_month,

            "next_year":
                next_year,

            "next_month":
                next_month,

        }

        return render(
            request,
            "admin/property_calendar.html",
            context
        )

    # =====================================================
    # TOGGLE DATE
    # =====================================================

    def toggle_date(self, request, object_id):

        if request.method != "POST":

            return redirect(
                "admin:property_calendar",
                object_id=object_id
            )

        property_obj = get_object_or_404(
            Property,
            pk=object_id
        )

        date_string = request.POST.get(
            "date"
        )

        try:

            selected_date = date.fromisoformat(
                date_string
            )

        except (ValueError, TypeError):

            messages.error(
                request,
                "التاريخ غير صحيح."
            )

            return redirect(
                "admin:property_calendar",
                object_id=object_id
            )

        # =================================================
        # هات اليوم أو أنشئه
        # =================================================

        property_date, created = PropertyDate.objects.get_or_create(

            property=property_obj,

            date=selected_date,

            defaults={
                "available": True
            }

        )

        # =================================================
        # اقلب الحالة
        # =================================================

        property_date.available = not property_date.available

        property_date.save()

        if property_date.available:

            messages.success(
                request,
                f"تم فتح يوم {selected_date.strftime('%d/%m/%Y')}."
            )

        else:

            messages.warning(
                request,
                f"تم إغلاق يوم {selected_date.strftime('%d/%m/%Y')}."
            )

        # =================================================
        # رجوع لنفس الشهر
        # =================================================

        return redirect(
            f"{reverse('admin:property_calendar', args=[property_obj.pk])}"
            f"?year={selected_date.year}"
            f"&month={selected_date.month}"
        )


# =========================================================
# PROPERTY DATE ADMIN
# =========================================================

@admin.register(PropertyDate)
class PropertyDateAdmin(admin.ModelAdmin):

    list_display = (
        "property",
        "date",
        "day_name",
        "available",
    )

    list_filter = (
        "available",
        "date",
    )

    search_fields = (
        "property__title",
    )

    ordering = (
        "date",
    )

    @admin.display(description="اليوم")
    def day_name(self, obj):

        names = [

            "الاثنين",
            "الثلاثاء",
            "الأربعاء",
            "الخميس",
            "الجمعة",
            "السبت",
            "الأحد",

        ]

        return names[
            obj.date.weekday()
        ]


# =========================================================
# BOOKING ADMIN
# =========================================================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "phone",
        "property",
        "booking_date",
        "booking_time",
        "guests_count",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "booking_date",
        "property",
    )

    search_fields = (
        "full_name",
        "phone",
        "property__title",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    list_editable = (
        "status",
    )