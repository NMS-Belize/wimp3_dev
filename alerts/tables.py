# tables.py
import django_tables2 as tables

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import localtime

from datetime import datetime

User = get_user_model()

from .models import CAPAlerts, TropicalWeatherAlertsCategory, TropicalWeatherAlerts

class TropicalWeatherALertsCategoryTable(tables.Table):

    edit        = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:40px;","class": "text-center"}, "td": {"style": "","class": "col_edit"}})
    delete      = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:40px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})
    id          = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:80px;","class": "col_id"}, "td": {"style": "","class": "col_id"}})
    
    category_name = tables.Column(verbose_name="Category Name", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})

    created_by          = tables.Column(verbose_name="Created By",attrs={"th": {"style": "width:120px;"},"td": {}})
    created_datetime    = tables.DateTimeColumn(verbose_name="Created Date",format="M d, Y h:i A", attrs={"th": {"style": "width:160px;",},"td": {"class": "fst-italic"}})

    updated_by          = tables.Column(verbose_name="Updated By",attrs={"th": {"style": "width:120px;"},"td": {}})
    updated_datetime    = tables.DateTimeColumn(verbose_name="Updated Date", format="M d, Y h:i A", attrs={ "th": { "style": "width:160px;", }, "td": {"class": "fst-italic"}})

    

    class Meta:
        model = TropicalWeatherAlertsCategory
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        attrs = {"class": "table table-striped table-condensed table-hover tbl_wimp3" }
        fields = ("edit","category_name","created_by","created_datetime","updated_by","updated_datetime","id","delete")
        order_by = "category_name"
        
    def render_edit(self, record):
        url = reverse("alerts:tropical_alerts_category_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_category_name(self, record):
        link_html = '<a href="{}" class="btn btn_edit_link p-0 text-decoration-none">{}</a>'
        url = reverse("alerts:tropical_alerts_category_entry", args=[record.id])
        return format_html(link_html, url, record.category_name)

    def render_created_by(self, record):
        if not record:
            return ""
        
        first_name  = f"{record.created_by.first_name[:1]}"
        last_name   = f"{record.created_by.last_name}"

        if first_name and last_name:
            return f"{first_name[0].upper()}. {last_name}"

        return record.created_by

    def render_updated_by(self, record):
        if not record:
            return ""
        
        first_name  = f"{record.updated_by.first_name[:1]}"
        last_name   = f"{record.updated_by.last_name}"

        if first_name and last_name:
            return f"{first_name[0].upper()}. {last_name}"

        return record.updated_by
    
    def render_delete(self, record):
        url = reverse("alerts:tropical_alerts_category_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class TropicalWeatherALertsTable(tables.Table):

    edit        = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:40px;","class": "text-center"}, "td": {"style": "","class": "col_edit"}})
    delete      = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:40px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})
    id          = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:80px;","class": "col_id"}, "td": {"style": "","class": "col_id"}})

    storm_name      = tables.Column(verbose_name="Storm Name", attrs={"th": {"style": "width:150px","class": ""}, "td": {"style": "","class": ""}})
    storm_category  = tables.Column(verbose_name="Storm Category", attrs={"th": {"style": "width:200px","class": ""}, "td": {"style": "","class": ""}})
    description     = tables.Column(verbose_name="Instructions Category", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})

    created_by          = tables.Column(verbose_name="Created By",attrs={"th": {"style": "width:120px;"},"td": {}})
    created_datetime    = tables.DateTimeColumn(verbose_name="Created Date",format="M d, Y h:i A", attrs={"th": {"style": "width:160px;",},"td": {"class": "fst-italic"}})

    updated_by          = tables.Column(verbose_name="Updated By",attrs={"th": {"style": "width:120px;"},"td": {}})
    updated_datetime    = tables.DateTimeColumn(verbose_name="Updated Date", format="M d, Y h:i A", attrs={ "th": { "style": "width:160px;", }, "td": {"class": "fst-italic"}})

    is_published = tables.TemplateColumn(verbose_name="Status", empty_values=(), template_name="tropical-alerts/publish_toggle.html",
                                attrs={ "th": {"style": "width:40px;","class": "text-center"}, "td": {"style": "","class": "text-center"}, }, orderable=False)
    
    class Meta:
        model = TropicalWeatherAlerts
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-striped table-condensed table-hover tbl_wimp3" }
        fields = ("edit","storm_name","storm_category","description","created_by","created_datetime","updated_by","updated_datetime","is_published","id","delete")
    
    def render_edit(self, record):
        url = reverse("alerts:tropical_alerts_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_description(self, value):
        short = value[:50] + "..." if len(value) > 50 else value
        return format_html('<span title="{}">{}</span>', value, short)

    def render_created_by(self, record):
        if not record:
            return ""
        
        first_name  = f"{record.created_by.first_name[:1]}"
        last_name   = f"{record.created_by.last_name}"

        if first_name and last_name:
            return f"{first_name[0].upper()}. {last_name}"

        return record.created_by

    def render_updated_by(self, record):
        if not record:
            return ""
        
        first_name  = f"{record.updated_by.first_name[:1]}"
        last_name   = f"{record.updated_by.last_name}"

        if first_name and last_name:
            return f"{first_name[0].upper()}. {last_name}"

        return record.updated_by
    
    def render_delete(self, record):
        url = reverse("alerts:tropical_alerts_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class CAPAlertsTable(tables.Table):
    guid        = tables.Column(verbose_name="GUID",    attrs={"th": {"style": "width:40px;","class": "text-center"}, "td": {"style": "","class": "text-center text-muted"}})
    title       = tables.Column(verbose_name="Title",   attrs={"th": {"style": "width:275px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Description", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    author      = tables.Column(verbose_name="Issued By", attrs={"th": {"style": "width: 120px","class": ""}, "td": {"style": "","class": ""}})
    
    pubdate     = tables.Column(verbose_name="Published Date", attrs={"th": {"style": "width:160px","class": ""}, "td": {"style": "","class": "fst-italic"}})

    is_published = tables.TemplateColumn(verbose_name="Status", empty_values=(), template_name="cap/publish_toggle.html",
                        attrs={ "th": {"style": "width:40px;","class": "text-center"}, "td": {"style": "","class": "text-center"}, }, orderable=False)
    
    view_details = tables.Column(verbose_name="Details", empty_values=(), attrs={ "th": {"style": "width:40px; text-align:center;","class": ""}, "td": {"style": "text-align:center;","class": "col_details"} })
    link        = tables.Column(verbose_name="URL",     attrs={"th": {"style": "width:40px;","class": ""}, "td": {"style": "","class": ""}})
    id          = tables.Column(verbose_name="ID",      attrs={"th": {"style": "width:80px;","class": "text-end",},"td": {"class": "text-end",}},  orderable=False,)
    
    class Meta:
        model = CAPAlerts
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("guid","title","description","author","pubdate","is_published","view_details","link","id")
        order_by = "-pubdate"

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_cap_alerts",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_guid(self, value):
        return format_html('<i class="fa-solid fa-circle-question" data-bs-toggle="tooltip" data-bs-placement="top" title="{}" style="cursor: pointer;"></i>', value)

    def render_pubdate(self, record):
        try:
            dt = datetime.strptime(record.pubdate,"%a, %d %b %Y %H:%M:%S %z")
            return dt.strftime("%d %b %Y %I:%M %p")

        except (ValueError, TypeError):
            return record.pubdate
    
    def render_link(self, record):
        url = record.link
        return format_html('<a href="{}" target="_blank" class="btn_edit"><i class="fa-solid fa-globe"></i></a>', url)

    def render_description(self, value):
            short = value[:50] + "..." if len(value) > 50 else value
            return format_html('<span title="{}">{}</span>', value, short)

    def render_author(self,record):

        author = record.author or ""
        username = author.split("@")[0].strip()

        user = User.objects.filter(username__iexact=username).first()

        if user:
            if user.first_name or user.last_name:
                return f"{user.last_name}"

            return user.username

        return username
    
    def render_view_details(self, record):
        url = reverse("alerts:cap_alerts_details", args=[record.id])
        return format_html('<a href="{}" class="btn_view_details"><i class="fa-solid fa-circle-info"></i></a>', url)
    
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