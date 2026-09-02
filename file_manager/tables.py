import django_tables2 as tables

from file_manager.models import Files

class FilesTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "col_edit"}, "td": {"style": "","class": "col_edit"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(attrs={"th": {"style": "width:700px;","class": ""}, "td": {"style": "","class": ""}})
    #sector = tables.Column(verbose_name="Sector", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = Files
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description", "id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    '''def render_edit(self, record):
        url = reverse("agro:commodity_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)

    def render_description(self, record):
        link_html = '<a href="{}" class="btn_link p-0 text-decoration-none">{}</a>'
        url = reverse("agro:commodity_entry", args=[record.id])
        return format_html(link_html, url, record.description)
    
    def render_delete(self, record):
        url = reverse("agro:commodity_type_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)'''