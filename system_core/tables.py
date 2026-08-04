# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

from .models import DepartmentSection, JobTitle, OfficeLocation, AlertLevel, RiskLevel, District

class DistrictTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    district_name = tables.Column(verbose_name="District Name", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = District
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","district_name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("system_core:district_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("system_core:district_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class AlertLevelTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Alert Level", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    color = tables.Column(verbose_name="Color")
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = AlertLevel
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description", "color","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_color(self, record):
        link_html = '<span><i class="fa-solid fa-square" style="color: {};"></i></span>'
        #url = reverse("system_core:alert_level_entry", args=[record.id])
        return format_html(link_html,record.color)
    
    def render_edit(self, record):
        url = reverse("system_core:alert_level_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_description(self, record):
        link_html = '<a href="{}" class="btn btn-link p-0 text-decoration-none">{}</a>'
        url = reverse("system_core:alert_level_entry", args=[record.id])
        return format_html(link_html, url, record.description)

    def render_delete(self, record):
        url = reverse("system_core:alert_level_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class RiskLevelTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Risk Alert Level", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    color = tables.Column(verbose_name="Color")
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center"}})

    class Meta:
        model = RiskLevel
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description", "color","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_color(self, record):
        return format_html('<span><i class="fa-solid fa-square" style="color: {};"></i></span>',record.color)
    
    def render_edit(self, record):
        url = reverse("system_core:risk_level_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("system_core:risk_level_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class JobTitleTable(tables.Table):
    edit    = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id      = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    description = tables.Column(verbose_name="Job Title",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete  = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = JobTitle
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","description","delete")
        sequence = ("edit","description","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("system_core:job_title_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("system_core:job_title_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class DepartmentSectionTable(tables.Table):
    edit    = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id      = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    name    = tables.Column(verbose_name="Department/Section Name",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    short_name = tables.Column(verbose_name="Short Name",attrs={"th": {"style": "width:140px;","class": ""}, "td": {"style": "","class": ""}})
    delete  = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = DepartmentSection
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","name","short_name","delete")
        sequence = ("edit","short_name","name","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("system_core:department_section_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("system_core:department_section_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class OfficeLocationTable(tables.Table):
    edit    = tables.Column(empty_values=(), verbose_name="Edit", orderable=False, attrs={"th": {"style": "width:60px;","class": "col_edit text-center"}, "td": {"style": "","class": "text-center col_edit"}})
    id      = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    name    = tables.Column(verbose_name="Office Location Name",attrs={"th": {"style": "width:350px;","class": ""}, "td": {"style": "","class": ""}})
    floor   = tables.Column(verbose_name="Floor",attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    description   = tables.Column(verbose_name="Description",attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete  = tables.Column(empty_values=(), verbose_name="Delete", orderable=False, attrs={"th": {"style": "width:75px;","class": "col_edit text-center"},"td": {"style": "","class": "col_delete text-center", }})

    class Meta:
        model = OfficeLocation
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","id","name","floor","description","delete")
        sequence = ("edit","name","floor","description","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("system_core:office_location_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("system_core:office_location_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)