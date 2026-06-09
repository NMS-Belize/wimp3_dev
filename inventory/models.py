from django.db import models

from django.conf import settings

class InventoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class DeviceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    inventory_category = models.ForeignKey(InventoryCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='device_types')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Device Types'

    def __str__(self):
        return self.name

class DepartmentSection(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    short_name  = models.CharField(max_length=25, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Department Sections'

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

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=25, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return self.name
    
class InventoryItem(models.Model):
    
    STATUS_CHOICES = [
        (1, 'Available'),
        (2, 'In Use'),
        (3, 'Under Maintenance'),
        (4, 'Damaged'),
        (5, 'Retired'),
    ]

    FLOOR_CHOICES = [
        ('1', 'Ground Floor'),
        ('2', 'Second Floor'),
        ('3', 'Third Floor'),
    ]
    
    device_label    = models.CharField(max_length=200, unique=True, null=False)
    device_name     = models.CharField(max_length=200, unique=True, null=False)
    device_type     = models.ForeignKey(DeviceType, on_delete=models.SET_NULL, blank=True, null=True)

    assigned_user   = models.CharField(max_length=100, unique=False)
    placement       = models.ForeignKey(OfficeLocationPlacement,on_delete=models.SET_NULL,related_name='items',blank=True,null=True)
    department_section = models.ForeignKey(DepartmentSection, on_delete=models.SET_NULL, blank=True, null=True)
    floor_level     = models.CharField(max_length=100, choices=FLOOR_CHOICES, blank=True, null=True)
    category        = models.ForeignKey(InventoryCategory,on_delete=models.PROTECT,related_name='items')
    vendor          = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    manufacturer    = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True)
    model_number    = models.CharField(max_length=100, blank=True, null=True)
    
    '''processor       = models.CharField(max_length=100, blank=True, null=True)
    ram             = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    disk            = models.CharField(max_length=100, blank=True, null=True)'''

    device_status   = models.IntegerField(max_length=20, choices=STATUS_CHOICES, default=1)
    serial_number   = models.CharField(max_length=150, blank=True, null=True)
    '''mac_address     = models.CharField(max_length=150, blank=True, null=True)
    ip_address      = models.CharField(max_length=150, blank=True, null=True)'''

    acquisition_date    = models.DateField(blank=True, null=True)
    date_issued         = models.DateField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="inventory_item_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="inventory_item_updated")

    class Meta:
        ordering = ['device_label']
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'

    def __str__(self):
        return f"{self.device_label} ({self.service_tag})"
    
class HardwareSpecifications(models.Model):
    inventory_item  = models.CharField(max_length=200, unique=True, null=False)
    service_tag     = models.CharField(max_length=30, blank=True, null=True)
    express_service_code = models.CharField(max_length=30, blank=True, null=True)
    processor       = models.CharField(max_length=100, blank=True, null=True)
    ram             = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    disk_size        = models.CharField(max_length=100, blank=True, null=True)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="hardware_specs_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="hardware_specs_updated")

    def __str__(self):
        return f"{self.inventory_item} Specs"

class NetworkDetails(models.Model):

    CABINET_CHOICES = [
        ('A', 'Cabinet A'),
        ('B', 'Cabinet B')
    ]

    inventory_item      = models.CharField(max_length=200, unique=True, null=False)
    mac_address         = models.CharField(max_length=150, blank=True, null=True)
    ip_address          = models.CharField(max_length=150, blank=True, null=True)
    switch_port_number  = models.CharField(max_length=150, blank=True, null=True)
    cabinet             = models.CharField(max_length=150, blank=True, null=True, choices=CABINET_CHOICES)
    rack_number         = models.CharField(max_length=150, blank=True, null=True)
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="network_details_created")
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="network_details_updated")

    class Meta:
        ordering = ['inventory_item']
        verbose_name = 'Network Details'
        verbose_name_plural = 'Network Details'

    def __str__(self):
        return f"{self.inventory_item} Network Details"