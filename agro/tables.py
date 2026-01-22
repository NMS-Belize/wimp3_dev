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
        fields = ("edit","description", "commodity_category","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("agro:commodity_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("agro:commodity_type_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class PestAlertLevelsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Pest Risk Alert", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    color_hex = tables.Column(verbose_name="Color")
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = PestAlertLevel
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description", "color_hex","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_color_hex(self, record):
        return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',record.color_hex)
    
    def render_edit(self, record):
        url = reverse("agro:pest_alert_level_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("agro:pest_alert_level_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class DroughtAlertLevelsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Drought Alert Level",attrs={"th": {"style": "width:250px;","class": ""}, "td": {"style": "","class": ""}})  # override column header
    color_hex = tables.Column(verbose_name="Color")  # override column header
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})
    
    class Meta:
        model = DroughtAlertLevel
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description", "color_hex","id")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-condensed table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }
    
    def render_color_hex(self, record):
        return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',record.color_hex)

    def render_edit(self, record):
        url = reverse("agro:drought_alert_level_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_delete(self, record):
        url = reverse("agro:drought_alert_level_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class ActionItemsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={
        "th": {"style": "width:75px;","class": "text-center"}, 
        "td": {"style": "","class": "col_edit text-center"}})
    
    id = tables.Column(verbose_name="ID",attrs={
        "th": {"style": "width:75px;","class": "text-center"}, 
        "td": {"style": "","class": "text-center"}
    })
    action_description = tables.Column(verbose_name="Description")  # override column header
    
    duplicate = tables.Column(empty_values=(),verbose_name="Duplicate",attrs={
        "th": {"style": "width:75px;", "class": "text-center"},
        "td": {"class": "col_edit text-center"},
    })  

    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})
    
    class Meta:
        model = PestRiskAction
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","action_description","duplicate","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "tbl_pest_risk_action",           # unique table ID
            "class": "table table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("agro:action_items_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_duplicate(self, record):
        url = reverse("agro:action_items_entry_duplicate", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_duplicate"><i class="fa-solid fa-copy"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("agro:action_items_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class EffectItemsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "text-center"}})
    effect_description = tables.Column(verbose_name="Description")  # override column header
    duplicate = tables.Column(empty_values=(),verbose_name="Duplicate",attrs={
        "th": {"style": "width:75px;", "class": "text-center"},
        "td": {"class": "text-center"},
    })   
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})

    #fields = ("id","effect_description", "duplicate")
    
    class Meta:
        model = PestRiskEffect
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","effect_description","duplicate","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("agro:effect_items_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i><a>', url)
    
    def render_duplicate(self, record):
        url = reverse("agro:effect_items_entry_duplicate", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_duplicate"><i class="fa-solid fa-copy"></i></a>', url)

    def render_delete(self, record):
        url = reverse("agro:effect_items_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
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
                        "th": {"style": "width:80px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    months_display  = tables.Column(empty_values=(),verbose_name="Months",attrs={
                        "th": {"style": "width:150px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    commodity       = tables.Column(accessor="commodity.description", verbose_name="Commodity",attrs={
        "th": {"style": ""},
        "td": {"class": "col_category"},
    })
    commodity_category = tables.Column(accessor="commodity.commodity_category", verbose_name="Sector",attrs={
        "th": {"style": ""},
        "td": {"class": ""},
    })

    edit            = tables.Column(empty_values=(), verbose_name="Edit",attrs={
                        "th": {"style": "width:60px;","class": ""},
                        "td": {"style": "","class": "col_edit"}
                        })
    view_details    = tables.Column(empty_values=(), verbose_name="View Details", attrs={
                        "th": {"style": "width:100px; text-align:center;","class": ""},
                        "td": {"style": "text-align:center;","class": "col_view"}
                        })
    '''add_details     = tables.Column(empty_values=(), verbose_name="Add Details", attrs={
                        "th": {"style": "width:90px; text-align:center;","class": ""},
                        "td": {"style": "text-align:center;","class": "col_details"}
                        })'''
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})

    class Meta:
        model = PestRiskEntryMainListing
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        #fields = ("edit", "year", "months_display", "commodity","commodity_category","view_details","add_details","id","delete")
        fields = ("edit", "year", "months_display", "commodity","commodity_category","view_details","id","delete")
        
        attrs = {
            "id": "tbl_pest_risk_listing",
            "class": "tbl_wimp3 table table-striped table-condensed table-hover tbl_wimp3",
        }

    def render_months_display(self, record):
        if record.months:
            return ", ".join(
                calendar.month_abbr[int(m)].upper()
                for m in record.months
            )
        return ""
    
    def render_edit(self, record):
        url = reverse("agro:pest_risk_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_view_details(self, record):
        url = reverse("agro:pest_risk_details_list", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_view"><i class="fa-solid fa-eye"></i></a>', url)
    
    '''def render_add_details(self, record):
        url = reverse("agro:pest_risk_details_create", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_add_details"><i class="fa-solid fa-plus"></i></a>', url)'''
    
    def render_delete(self, record):
        url = reverse("agro:pest_risk_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class PestRiskDetailsTable(tables.Table):

    edit            = tables.Column(empty_values=(), verbose_name="Edit",attrs={
                        "th": {"style": "width:50px;","class": "col_edit"},
                        "td": {"style": "","class": "col_edit"}
                        })

    id              = tables.Column(verbose_name="ID",attrs={
                        "th": {"style": "width:60px; text-align:right;","class": "col_id"},
                        "td": {"style": "text-align:right;","class": "col_id"}
                        })
    district_id         = tables.Column(verbose_name="District / Zone",attrs={
                        "th": {"style": "width:160px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    pest_alert_lvl_id    = tables.Column(verbose_name="Pest Alert",attrs={
                        "th": {"style": "width:60px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    drought_alert_lvl_id    = tables.Column(verbose_name="Drought Alert", attrs={
                        "th": {"style": "width:60px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    temp_min            = tables.Column(verbose_name="TEMP °F (MIN)", attrs={
                        "th": {"style": "width:80px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    temp_max            = tables.Column(verbose_name="TEMP °F (MAX)", attrs={
                        "th": {"style": "width:75px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    precip_min            = tables.Column(verbose_name="PRECIP mm (MIN)", attrs={
                        "th": {"style": "width:75px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    precip_max            = tables.Column(verbose_name="PRECIP mm (MAX)", attrs={
                        "th": {"style": "width:75px; text-align:right;","class": ""},
                        "td": {"style": "text-align:right;","class": ""}
                        })
    effect            = tables.Column(attrs={
                        "th": {"style": "","class": ""},
                        "td": {"style": "","class": ""}
                        })
    info            = tables.Column(attrs={
                        "th": {"style": ";","class": ""},
                        "td": {"style": "","class": ""}
                        })
    actions            = tables.Column(attrs={
                        "th": {"style": "","class": ""},
                        "td": {"style": "","class": ""}
                        })
    
    duplicate = tables.Column(empty_values=(),verbose_name="Duplicate",attrs={
        "th": {"style": "width:75px;", "class": "text-center"},
        "td": {"class": "text-center"},
    }) 
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})
    

    class Meta:
        model = PestRiskEntryDetails
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields = ("edit", "district_id", "pest_alert_lvl_id", "drought_alert_lvl_id","temp_min","temp_max","precip_min","precip_max","effect","info","actions","duplicate","id","delete")
        
        # Add table ID and class here
        attrs = {
            "id": "tbl_pest_risk_listing",
            "class": "tbl_wimp3 table table-striped table-condensed table-hover tbl_wimp3",
        }

    def render_edit(self, record):
        url = reverse("agro:pest_risk_details_entry",args=[record.pest_risk_listing_id_id, record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_pest_alert_lvl_id(self, value, record):
        color = value.color_hex if value.color_hex else "#000"  # fallback black
        return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',color,value.description)
    
    def render_drought_alert_lvl_id(self, value, record):
        color = value.color_hex if value.color_hex else "#000"  # fallback black
        return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',color,value.description)
    
    def render_duplicate(self, record):
        url = reverse("agro:pest_risk_details_entry_duplicate", args=[record.pest_risk_listing_id_id, record.id])
        return format_html('<a href="{}" class="btn_duplicate"><i class="fa-solid fa-copy"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("agro:pest_risk_details_delete", args=[record.pest_risk_listing_id_id, record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    

    #def render_color_hex(self, record):
    #    return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',record.color_hex)