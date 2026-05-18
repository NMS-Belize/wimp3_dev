# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

from .models import InventoryItem, InventoryCategory, OfficeLocationPlacement

class InventoryCategoryTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    name = tables.Column(verbose_name="Category Name",attrs={"th": {"style": "width:300px;","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = InventoryCategory
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:inventory_category_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("inventory:inventory_category_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class InventoryTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="District",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})

    class Meta:
        model = InventoryItem
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("agro:sector_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("agro:sector_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    