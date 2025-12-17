# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

#from .models import PestRiskEntryMainListing, PestRiskEntryDetails, Months, PestAlertLevel, PestRiskAction, PestRiskEffect
from .models import *

class CommodityTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(attrs={"th": {"style": "width:700px;","class": ""}, "td": {"style": "","class": ""}})
    commodity_category = tables.Column(verbose_name="Commodity Category", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = CommodityType
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","description", "commodity_category","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("commodity_entry", args=[record.id])
        return format_html('<a href="{}" class="btn btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("commodity_type_delete", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class PestAlertLevelsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Pest Risk Alert", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    color_hex = tables.Column(verbose_name="Color Hex #")
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = PestAlertLevel
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","description", "color_hex","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("pest_alert_level_entry", args=[record.id])
        return format_html('<a href="{}" class="btn btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("pest_alert_level_delete", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class DroughtAlertLevelsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Pest Risk Alert")  # override column header
    color_hex = tables.Column(verbose_name="Color Hex #")  # override column header
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = PestAlertLevel
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("id","description", "color_hex")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("pest_risk_levels_table", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_delete(self, record):
        url = reverse("pest_alert_level_update", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class ActionItemsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    action_description = tables.Column(verbose_name="Description")  # override column header
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    fields = ("id","action_description")
    
    class Meta:
        model = PestRiskAction
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","action_description","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("action_items_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_delete(self, record):
        url = reverse("action_items_delete", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class EffectItemsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    effect_description = tables.Column(verbose_name="Description")  # override column header
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    fields = ("id","effect_description")
    
    class Meta:
        model = PestRiskEffect
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","effect_description","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("effect_items_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_delete(self, record):
        url = reverse("effect_items_delete", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class PestRiskListTable(tables.Table):
    class Meta:
        model = PestRiskEntryDetails
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields = ("id","pest_risk_listing_id", "district_id", "pest_alert_lvl_id", "drought_alert_lvl_id", "temp_max", "temp_min", "precip_min", "precip_max", "effect", "info", "actions")

class PestRiskMainListTable(tables.Table):
    id              = tables.Column(verbose_name="ID",attrs={
                        "th": {"style": "width:5%; text-align:center;","class": "col_id"},
                        "td": {"style": "text-align:center;","class": "col_id"}
                        })
    year            = tables.Column(attrs={
                        "th": {"style": "width:15%;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    commodity       = tables.Column(accessor="commodity.description", verbose_name="Commodity")
    months_display  = tables.Column(verbose_name="Months")
    edit            = tables.Column(empty_values=(), verbose_name="Edit",attrs={
                        "th": {"style": "width:5%;","class": "col_edit"},
                        "td": {"style": "","class": "col_edit"}
                        })
    view_details    = tables.Column(empty_values=(), verbose_name="View Details", attrs={
                        "th": {"style": "width:5%; text-align:center;","class": "col_view"},
                        "td": {"style": "text-align:center;","class": "col_view"}
                        })
    add_details     = tables.Column(empty_values=(), verbose_name="Add Details", attrs={
                        "th": {"style": "width:5%; text-align:center;","class": "col_details"},
                        "td": {"style": "text-align:center;","class": "col_details"}
                        })

    class Meta:
        model = PestRiskEntryMainListing
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields = ("edit", "year", "months_display", "commodity","view_details","add_details","id")
        # Add table ID and class here
        attrs = {
            "id": "tbl_pest_risk_listing",
            "class": "tbl_wimp3 table",
        }

    '''def render_months_display(self, record):
        month_map = {
            "1": "JAN", "2": "FEB", "3": "MAR", "4": "APR",
            "5": "MAY", "6": "JUN", "7": "JUL", "8": "AUG",
            "9": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"
        }
        if obj.months:
            return ", ".join([month_map.get(str(m), f"Unknown({m})") for m in obj.months])
        return "N/A"'''
    
    def render_edit(self, record):
        url = reverse("pest_risk_details_list", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_view_details(self, record):
        url = reverse("pest_risk_details_list", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_view"><i class="fa-solid fa-eye"></i></a>', url)
    
    def render_add_details(self, record):
        url = reverse("pest_risk_details_list", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_add_details"><i class="fa-solid fa-plus"></i></a>', url)
    
class PestRiskDetailsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit")
    pest_alert_lvl_id = tables.Column(verbose_name="Pest Risk Alert")  # override column header
    drought_alert_lvl_id = tables.Column(verbose_name="Drought Alert")  # override column header
    temp_min = tables.Column(verbose_name="TEMP MIN")  # override column header
    temp_max = tables.Column(verbose_name="TEMP MAX")  # override column header

    class Meta:
        model = PestRiskEntryDetails
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("id","district_id", "pest_alert_lvl_id", "drought_alert_lvl_id","temp_min","temp_max","precip_min","precip_max","pest_risk_listing_id")

    def render_edit(self, record):
        url = reverse("pest_risk_entry_details", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn btn-sm btn-primary">Edit</a>', url)