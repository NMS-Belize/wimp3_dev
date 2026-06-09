# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

from .models import DepartmentSection, DeviceType, InventoryItem, InventoryCategory, Manufacturer, Vendor

class InventoryCategoryTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    name = tables.Column(verbose_name="Category Name",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = InventoryCategory
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","name","delete")
        sequence = ("edit","name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:inventory_category_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("inventory:inventory_category_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class DeviceTypeTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    name = tables.Column(verbose_name="Device Type Name",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = DeviceType
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","name","delete")
        sequence = ("edit","name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:device_type_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("inventory:device_type_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class DepartmentSectionTable(tables.Table):
    edit    = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id      = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    name    = tables.Column(verbose_name="Department/Section Name",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    short_name = tables.Column(verbose_name="Short Name",attrs={"th": {"style": "width:140px;","class": ""}, "td": {"style": "","class": ""}})
    delete  = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = DepartmentSection
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","name","short_name","delete")
        sequence = ("edit","short_name","name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:department_section_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("inventory:department_section_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class ManufacturerTable(tables.Table):
    edit    = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id      = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    name    = tables.Column(verbose_name="Manufacturer Name",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete  = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = Manufacturer
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","name","delete")
        sequence = ("edit","name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:manufacturer_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("inventory:manufacturer_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class VendorTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    name = tables.Column(verbose_name="Vendor Name",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    short_name = tables.Column(verbose_name="Short Name",attrs={"th": {"style": "width:180px;","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = Vendor
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","name","short_name","delete")
        sequence = ("edit","name","short_name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:vendor_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("inventory:vendor_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class InventoryTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    device_label = tables.Column(verbose_name="Device Label",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    device_name = tables.Column(verbose_name="Device Name",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})

    class Meta:
        model = InventoryItem
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","device_label","device_name","delete")
        sequence = ("edit","device_label","device_name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:inventory_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("inventory:inventory_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    