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