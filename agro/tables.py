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
                        "th": {"style": "width:60px; text-align:right;","class": "col_id"},
                        "td": {"style": "text-align:right;","class": "col_id"}
                        })
    year            = tables.Column(attrs={
                        "th": {"style": "width:150px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    months_display  = tables.Column(empty_values=(),verbose_name="Months",attrs={
                        "th": {"style": "width:300px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    commodity       = tables.Column(accessor="commodity.description", verbose_name="Commodity")
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
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = PestRiskEntryMainListing
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields = ("edit", "year", "months_display", "commodity","view_details","add_details","id","delete")
        
        attrs = {
            "id": "tbl_pest_risk_listing",
            "class": "tbl_wimp3 table",
        }

    def render_months_display(self, record):
        if record.months:
            return ", ".join(
                calendar.month_abbr[int(m)].upper()
                for m in record.months
            )
        return ""
    
    def render_edit(self, record):
        url = reverse("pest_risk_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_view_details(self, record):
        url = reverse("pest_risk_details_list", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_view"><i class="fa-solid fa-eye"></i></a>', url)
    
    def render_add_details(self, record):
        url = reverse("pest_risk_details_create", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_add_details"><i class="fa-solid fa-plus"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("pest_risk_delete", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class PestRiskDetailsTable(tables.Table):

    id              = tables.Column(verbose_name="ID",attrs={
                        "th": {"style": "width:60px; text-align:right;","class": "col_id"},
                        "td": {"style": "text-align:right;","class": "col_id"}
                        })
    district_id            = tables.Column(verbose_name="District / Zone",attrs={
                        "th": {"style": "width:250px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    pest_alert_lvl_id    = tables.Column(verbose_name="Pest Alert",attrs={
                        "th": {"style": "width:160px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    drought_alert_lvl_id    = tables.Column(verbose_name="Drought Alert", attrs={
                        "th": {"style": "width:160px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    temp_min            = tables.Column(verbose_name="TEMP °F (MIN)", attrs={
                        "th": {"style": "width:140px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    temp_max            = tables.Column(verbose_name="TEMP °F (MAX)", attrs={
                        "th": {"style": "width:140px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    precip_min            = tables.Column(verbose_name="PRECIP (MIN), mm", attrs={
                        "th": {"style": "width:160px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    precip_max            = tables.Column(verbose_name="PRECIP (MAX), mm", attrs={
                        "th": {"style": "width:160px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    effect            = tables.Column(attrs={
                        "th": {"style": "","class": ""},
                        "td": {"style": "","class": ""}
                        })
    info            = tables.Column(attrs={
                        "th": {"style": "","class": ""},
                        "td": {"style": "","class": ""}
                        })
    actions            = tables.Column(attrs={
                        "th": {"style": "width:80px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    edit            = tables.Column(empty_values=(), verbose_name="Edit",attrs={
                        "th": {"style": "width:80px;","class": "col_edit"},
                        "td": {"style": "","class": "col_edit"}
                        })

    class Meta:
        model = PestRiskEntryDetails
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields = ("edit", "district_id", "pest_alert_lvl_id", "drought_alert_lvl_id","temp_min","temp_max","precip_min","precip_max","effect","info","actions","id")
        
        # Add table ID and class here
        attrs = {
            "id": "tbl_pest_risk_listing",
            "class": "tbl_wimp3 table",
        }

    def render_edit(self, record):
        url = reverse("pest_risk_details_entry",args=[record.pest_risk_listing_id_id, record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)