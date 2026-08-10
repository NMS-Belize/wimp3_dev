from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_user_model

import django_tables2 as tables

User = get_user_model()

class UserTable(tables.Table):

    edit        = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id          = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    first_name  = tables.Column(verbose_name="First Name", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    last_name   = tables.Column(verbose_name="Last Name", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    email       = tables.Column(verbose_name="Email", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})

    is_active   = tables.TemplateColumn(template_name="users/user_active_toggle.html", verbose_name="Active", orderable=False, 
                            attrs={"th": {"style": "width:75px;", "class": "text-center "},
                                   "td": {"style": "","class": "text-center"}})

    is_staff   = tables.TemplateColumn(template_name="users/user_staff_toggle.html", verbose_name="Django", orderable=False, 
                                attrs={"th": {"style": "width:75px;", "class": "text-center "},
                                       "td": {"style": "","class": "text-center"}})

    delete      = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center col_delete"},"td": {"style": "","class": "text-center col_delete"}})
    
    class Meta:
        model = User
        fields = ( "id","username","first_name","last_name","email","is_active","is_staff")
        sequence = ("edit","username","first_name","last_name","email","is_active","is_staff","id")
        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_users",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("users:user_entry_details", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_delete(self, record):
            url = reverse("users:user_delete", args=[record.id])
            return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class EmployeeTable(tables.Table):

    edit        = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id          = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    first_name  = tables.Column(verbose_name="First Name", attrs={"th": {"style": "width:150px","class": ""}, "td": {"style": "","class": ""}})
    last_name   = tables.Column(verbose_name="Last Name", attrs={"th": {"style": "width:150px","class": ""}, "td": {"style": "","class": ""}})
    email       = tables.Column(verbose_name="Email", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    job_title   = tables.Column(verbose_name="Job Title", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    department  = tables.Column(verbose_name="Department", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    phone       = tables.Column(verbose_name="Phone", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    office_location = tables.Column(verbose_name="Office Location", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete      = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "text-center col_delete"},"td": {"style": "","class": "text-center col_delete"}})
    
    class Meta:
        model = User
        fields = ( "id","first_name","last_name","email","phone","department","office_location","job_title")
        sequence = ("edit","first_name","last_name","job_title","department","office_location","email","phone","id")
        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_users",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        url = reverse("users:employee_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_delete(self, record):
            url = reverse("users:employee_delete", args=[record.id])
            return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)