# tables.py
import django_tables2 as tables
import calendar

from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html

from .models import WeatherIcons, WeatherCodes

class WeatherIconsTable(tables.Table):
    
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit align-middle"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": "align-middle"}})
    name = tables.Column(verbose_name="Name",attrs={"th": {"style": "width:300px;","class": ""}, "td": {"style": "","class": "align-middle"}})
    image_day = tables.Column(verbose_name="Icon (DAY)",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": "align-middle"}})
    image_night = tables.Column(verbose_name="Icon (NIGHT)",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": "align-middle"}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete align-middle"}})

    class Meta:
        model = WeatherIcons
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","name","image_day","image_night","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }
    def render_edit(self, record):
        url = reverse("observations:weather_icon_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_name(self, record):
        url = reverse("observations:weather_icon_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit">{}</a>', url, record.name)
    
    def render_image_day(self, value):
        if value:
            return format_html('<img src="{}" alt="Icon" style="max-width: 50px; max-height:50px;" />', static(str(value)))
        return ""

    def render_image_night(self, value):
        if value:
            return format_html('<img src="{}" alt="Icon" style="max-width: 50px; max-height: 50px;" />', static(str(value)))
        return ""

    def render_delete(self, record):
        url = reverse("observations:weather_icon_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    

class WeatherCodesTable(tables.Table):
    
    edit    = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id      = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    code    = tables.Column(verbose_name="Code",attrs={"th": {"style": "width:100px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Description",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    icon_file = tables.Column(verbose_name="Icon File",attrs={"th": {"style": "width:300px;","class": ""}, "td": {"style": "","class": ""}})
    delete  = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = WeatherCodes
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","code","description","icon_file","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("inventory:inventory_category_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    '''def render_icon_file(self, value):
        if value:
            return format_html('<img src="{}" alt="Icon" style="max-width: 35px; max-height: 35px;" />', value.icon_file)
        return ""'''

    def render_delete(self, record):
        url = reverse("inventory:inventory_category_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)