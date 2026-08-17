# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

from agro.models import PestRiskEntryDetails, Months, PestAlertLevel, PestRiskAction, PestRiskEffect, Sector, DroughtAlertLevel, Commodity, PestRiskInfo
from system_core.models import District

class SectorTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="District",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})

    class Meta:
        model = Sector
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
    


class DistrictZoneTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    district_area = tables.Column(verbose_name="District",attrs={"th": {"style": "width:300px;","class": ""}, "td": {"style": "","class": ""}})
    zone_id = tables.Column(verbose_name="Zone/Area", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = District
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","district_area","zone_id","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("agro:commodity_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("agro:district_zone_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class CommodityTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(attrs={"th": {"style": "width:700px;","class": ""}, "td": {"style": "","class": ""}})
    sector = tables.Column(verbose_name="Sector", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = Commodity
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description", "sector","id","delete")

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
    edit        = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:50px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id          = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:80px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})

    action_description = tables.Column(verbose_name="Description")  # override column header
    commodity   = tables.Column(verbose_name="Commodity", attrs={"th": {"style": "width:100px","class": ""}, "td": {"style": "","class": ""}})

    duplicate   = tables.Column(empty_values=(),verbose_name="Duplicate",attrs={ "th": {"style": "width:50px;", "class": "text-center"}, "td": {"class": "text-center"} })  
    delete      = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})
    
    class Meta:
        model = PestRiskAction
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","action_description","commodity","duplicate","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_risk_info",
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
    edit        = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:50px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id          = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:80px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})

    effect_description = tables.Column(verbose_name="Description")  # override column header
    commodity   = tables.Column(verbose_name="Commodity", attrs={"th": {"style": "width:100px","class": ""}, "td": {"style": "","class": ""}})

    duplicate   = tables.Column(empty_values=(),verbose_name="Duplicate",attrs={ "th": {"style": "width:50px;", "class": "text-center"}, "td": {"class": "text-center"} })   
    delete      = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:50px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})
    
    class Meta:
        model = PestRiskInfo
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","effect_description","commodity","duplicate","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_risk_info",           # unique table ID
            "class": "table table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("agro:effect_items_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i><a>', url)

    def render_effect_description(self, value):
            short = value[:200] + "..." if len(value) > 200 else value
            return format_html('<span title="{}">{}</span>', value, short)
    
    def render_duplicate(self, record):
        url = reverse("agro:effect_items_entry_duplicate", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_duplicate"><i class="fa-solid fa-copy"></i></a>', url)

    def render_delete(self, record):
        url = reverse("agro:effect_items_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class InfoItemsTable(tables.Table):
    edit        = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:50px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id          = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:80px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})

    info_description = tables.Column(verbose_name="Description")  # override column header
    commodity   = tables.Column(verbose_name="Commodity", attrs={"th": {"style": "width:100px","class": ""}, "td": {"style": "","class": ""}})

    duplicate   = tables.Column(empty_values=(),verbose_name="Duplicate",attrs={ "th": {"style": "width:50px;", "class": "text-center"}, "td": {"class": "text-center"} })   
    delete      = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:50px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})
    
    class Meta:
        model = PestRiskInfo
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","info_description","commodity","duplicate","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_risk_info", 
            "class": "table table-striped table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("agro:info_items_entry", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i><a>', url)

    def render_info_description(self, value):
            short = value[:200] + "..." if len(value) > 200 else value
            return format_html('<span title="{}">{}</span>', value, short)
    
    def render_duplicate(self, record):
        url = reverse("agro:info_items_entry_duplicate", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_duplicate"><i class="fa-solid fa-copy"></i></a>', url)

    def render_delete(self, record):
        url = reverse("agro:info_items_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class PestRiskMainListTable(tables.Table):
    id          = tables.Column(verbose_name="ID", attrs={"th": {"style": "width:60px; text-align:right;","class": "col_id"},"td": {"style": "text-align:right;","class": "col_id"}})
    description = tables.Column(verbose_name="Commodity", accessor="description", attrs={"th": {"style": "","class": ""},"td": {"class": "col_category"}})
    sector      = tables.Column(verbose_name="Sector", accessor="sector", attrs={"th": {"style": ""},"td": {"class": ""}})
    view_details = tables.Column(verbose_name="Details", orderable=False, empty_values=(), attrs={"th": {"style": "width:70px; text-align:center;","class": ""}, "td": {"style": "text-align:center;","class": "col_view"}})

    class Meta:
        model = Commodity
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields = ("view_details","description","sector","id")
        sequence = fields
        
        attrs = {
            "id": "tbl_pest_risk_listing",
            "class": "tbl_wimp3 table table-striped table-condensed table-hover",
        }

    def render_view_details(self, record):
        url = reverse("agro:pest_risk_details_list", args=[record.id])  # change "pest_edit" to your URL name
        return format_html('<a href="{}" class="btn_view"><i class="fa-solid fa-list"></i></a>', url)

    def render_description(self, record):
        url = reverse("agro:pest_risk_details_list", args=[record.id]) 
        return format_html('<a href="{}" class="btn btn_edit_link p-0">{}</a>', url, record.description)
    
class PestRiskDetailsTable(tables.Table):

    edit            = tables.Column(empty_values=(), verbose_name="Edit",attrs={
                        "th": {"style": "width:50px;","class": "col_edit text-center"},
                        "td": {"style": "","class": "col_edit text-center"}
                        })

    id              = tables.Column(verbose_name="ID",attrs={
                        "th": {"style": "width:60px; text-align:right;","class": "col_id"},
                        "td": {"style": "text-align:right;","class": "col_id"}
                        })
    district_id         = tables.Column(verbose_name="District",attrs={
                        "th": {"style": "width:120px;","class": ""},
                        "td": {"style": "","class": ""}
                        })
    commodity_id         = tables.Column(verbose_name="Commodity",attrs={
                            "th": {"style": "width:120px;","class": ""},
                            "td": {"style": "","class": ""}
                            })
    pest_alert_lvl_id    = tables.Column(verbose_name="Pest Alert",attrs={
                        "th": {"style": "width:60px;","class": "text-center"},
                        "td": {"style": "","class": "text-center"}
                        })
    drought_alert_lvl_id    = tables.Column(verbose_name="Drought Alert", attrs={
                        "th": {"style": "width:60px;","class": "text-center"},
                        "td": {"style": "","class": "text-center"}
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
    is_published = tables.TemplateColumn(verbose_name="Published", template_name="tables/publish_toggle.html", orderable=False, attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "text-center"}})

    '''duplicate = tables.Column(empty_values=(),verbose_name="Duplicate",attrs={
        "th": {"style": "width:75px;", "class": "text-center"},
        "td": {"class": "text-center"},
    }) '''
    #delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "col_delete text-center"}})
    

    class Meta:
        model = PestRiskEntryDetails
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields = ("edit", "district_id", "commodity_id", "pest_alert_lvl_id", "drought_alert_lvl_id","temp_min","temp_max","precip_min","precip_max","effect","info","actions","is_published","id")
        
        # Add table ID and class here
        attrs = {
            "id": "tbl_pest_risk_listing",
            "class": "tbl_wimp3 table table-striped table-condensed table-hover tbl_wimp3",
        }

    def render_edit(self, record):
        url = reverse("agro:pest_risk_details_entry",args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_district(self, record):
        url = reverse("agro:pest_risk_details_entry", args=[record.id]) 
        return format_html('<a href="{}" class="btn btn_edit_link p-0">{}</a>', url, record.district)
    
    def render_pest_alert_lvl_id(self, value, record):
        color = value.color if value.color else "#000"  # fallback black
        return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',color,value.description)
    
    def render_drought_alert_lvl_id(self, value, record):
        color = value.color_hex if value.color_hex else "#000"  # fallback black
        return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',color,value.description)
    
    '''def render_duplicate(self, record):
        url = reverse("agro:pest_risk_details_entry_duplicate", args=[record.pest_risk_id_id, record.id])
        return format_html('<a href="{}" class="btn_duplicate"><i class="fa-solid fa-copy"></i></a>', url)'''
    
    '''def render_delete(self, record):
        url = reverse("agro:pest_risk_details_delete", args=[record.pest_risk_id_id, record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
    #def render_color_hex(self, record):
    #    return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',record.color_hex)'''