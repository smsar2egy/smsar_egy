from django.db import models


# =========================
# PROPERTY
# =========================

class Property(models.Model):

    PROPERTY_TYPES = [
        ('sale', 'للبيع'),
        ('rent', 'للإيجار'),
    ]

    CATEGORIES = [
        ('apartment', 'شقق'),
        ('villa', 'فلل'),
        ('chalet', 'شاليهات'),
        ('summer', 'مصايف'),
        ('property', 'عقارات'),
    ]

    LOCATIONS = [
        ('cairo', 'القاهرة'),
        ('giza', 'الجيزة'),
        ('north_coast', 'الساحل الشمالي'),
        ('hurghada', 'الغردقة'),
        ('dahab', 'دهب'),
        ('sharm', 'شرم الشيخ'),
        ('ain_sokhna', 'العين السخنة'),
    ]

    title = models.CharField(
        max_length=200
    )

    property_type = models.CharField(
        max_length=10,
        choices=PROPERTY_TYPES
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORIES
    )

    location = models.CharField(
        max_length=50,
        choices=LOCATIONS
    )

    description = models.TextField()

    area = models.PositiveIntegerField(
        help_text='المساحة بالمتر'
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    bedrooms = models.PositiveIntegerField(
        default=0
    )

    bathrooms = models.PositiveIntegerField(
        default=0
    )

    # الصورة الرئيسية
    image = models.ImageField(
        upload_to='properties/',
        blank=True,
        null=True
    )

    available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================
# PROPERTY IMAGES
# =========================

class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='properties/gallery/'
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text='ترتيب الصورة'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.property.title} - صورة {self.id}'


# =========================
# PROPERTY DATE
# =========================

class PropertyDate(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='dates'
    )

    date = models.DateField()

    available = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['date']
        unique_together = ('property', 'date')

    def __str__(self):

        status = (
            'متاح'
            if self.available
            else 'غير متاح'
        )

        return f'{self.property.title} - {self.date} - {status}'


# =========================
# BOOKING
# =========================

class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('confirmed', 'تم التأكيد'),
        ('cancelled', 'ملغي'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=30
    )

    guests_count = models.PositiveIntegerField(
        default=1
    )

    id_card = models.ImageField(
        upload_to='id_cards/',
        blank=True,
        null=True
    )

    booking_date = models.DateField()

    booking_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.full_name} - {self.property.title}'