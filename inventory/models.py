from django.db import models

class InventoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class OfficeLocationPlacement(models.Model):
    name = models.CharField(max_length=150, unique=True)
    building = models.CharField(max_length=150, blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        parts = [self.name]
        if self.building:
            parts.append(self.building)
        if self.room:
            parts.append(f"Room {self.room}")
        return " - ".join(parts)

class InventoryItem(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('damaged', 'Damaged'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=200)
    asset_tag = models.CharField(max_length=100, unique=True)
    serial_number = models.CharField(max_length=150, blank=True, null=True)

    category = models.ForeignKey(
        InventoryCategory,
        on_delete   =models.PROTECT,
        related_name='items'
    )
    placement = models.ForeignKey(
        OfficeLocationPlacement,
        on_delete   =models.SET_NULL,
        related_name='items',
        blank       =True,
        null        =True
    )

    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    acquisition_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_active = models.BooleanField(default=True)
    sponsor = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'

    def __str__(self):
        return f"{self.name} ({self.asset_tag})"