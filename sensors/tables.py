# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

#from .models import PestRiskEntryMainListing, PestRiskEntryDetails, Months, PestAlertLevel, PestRiskAction, PestRiskEffect
from .models import *
    
class RadarImagesTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    image_title = tables.Column(attrs={"th": {"style": "width:700px;","class": ""}, "td": {"style": "","class": ""}})
    image_url = tables.Column(verbose_name="Commodity Category", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = RadarImages
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","image_title", "image_url","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("radar_images", args=[record.id])
        return format_html('<a href="{}" class="btn btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("commodity_type_delete", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)