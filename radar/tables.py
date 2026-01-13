# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

#from .models import PestRiskEntryMainListing, PestRiskEntryDetails, Months, PestAlertLevel, PestRiskAction, PestRiskEffect
from .models import RadarImages
    
class RadarImagesTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    image_title = tables.Column(verbose_name="Image Title", attrs={"th": {"style": "width:700px;","class": ""}, "td": {"style": "","class": ""}})
    image_url = tables.Column(verbose_name="Image URL", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = RadarImages
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","image_title", "image_url","is_published","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_radar_images",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("radar:radar_image_entry", args=[record.id])
        return format_html('<a href="{}" class="btn btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("radar:radar_image_delete", args=[record.id])
        return format_html('<a href="{}" class="btn btn_delete"><i class="fa-solid fa-trash"></i></a>', url)