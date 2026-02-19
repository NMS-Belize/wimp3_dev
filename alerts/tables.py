# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import localtime

from datetime import datetime



#from .models import PestRiskEntryMainListing, PestRiskEntryDetails, Months, PestAlertLevel, PestRiskAction, PestRiskEffect
from .models import CAPAlerts
    
class CAPAlertsTable(tables.Table):
    guid = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    title = tables.Column(verbose_name="Title", attrs={"th": {"style": "width:250px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Description", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    author = tables.Column(verbose_name="Author", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    link = tables.Column(verbose_name="URL", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    pubdate = tables.Column(verbose_name="Published Date", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    is_published = tables.TemplateColumn(
        template_name="tables/publish_cap_toggle.html",
        verbose_name="Published",
        orderable=False,
        attrs={
            "th": {"style": "width:75px;","class": "text-center"},
            "td": {"style": "","class": "text-center"}
        })
    view_details = tables.Column(
        empty_values=(), 
        verbose_name="Details",
        orderable=False,
        attrs={
            "th": {"style": "width:100px; text-align:center;","class": ""},
            "td": {"style": "text-align:center;","class": "col_view"}
        })
    
    class Meta:
        model = CAPAlerts
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("guid","title","description","author","pubdate","link","is_published","view_details")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_cap_alerts",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }
    
    
    def render_link(self, record):
        url = record.link
        return format_html('<a href="{}" target="_blank" class="btn_edit"><i class="fa-solid fa-globe"></i></a>', url)
    
    def render_view_details(self, record):
        url = reverse("alerts:cap_alerts_details", args=[record.guid])
        return format_html('<a href="{}" class="btn_view_details"><i class="fa-solid fa-eye"></i></a>', url)
    
class CAPAlertsDetailsTable(tables.Table):
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    title = tables.Column(verbose_name="Title", attrs={"th": {"style": "width:250px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Description", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    author = tables.Column(verbose_name="Author", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    '''is_published = tables.TemplateColumn(
        template_name="tables/publish_toggle.html",
        verbose_name="Published",
        orderable=False,
        attrs={
            "th": {"style": "width:75px;","class": "text-center"},
            "td": {"style": "","class": "text-center"}
        })'''
    view_details = tables.Column(
        empty_values=(), 
        verbose_name="Details",
        orderable=False,
        attrs={
            "th": {"style": "width:100px; text-align:center;","class": ""},
            "td": {"style": "text-align:center;","class": "col_view"}
        })
    
    class Meta:
        model = CAPAlerts
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("title","description","author","link","is_published","view_details","id")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_cap_alerts",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_view_details(self, record):
        url = reverse("alerts:cap_alerts_details", args=[record.id])
        return format_html('<a href="{}" class="btn_view_details"><i class="fa-solid fa-eye"></i></a>', url)