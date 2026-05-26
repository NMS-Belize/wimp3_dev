# tables.py
import django_tables2 as tables
import calendar

from django.urls import reverse
from django.utils.html import format_html

from forecasts.models import AlertLevel, District, DistrictForecastDetails, DistrictForecastInstructions, RiskLevel, Severity, Probability, DistrictForecast

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
        url = reverse("forecasts:district_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("forecasts:district_delete", args=[record.id])
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
        #url = reverse("forecasts:alert_level_entry", args=[record.id])
        return format_html(link_html,record.color)
    
    def render_edit(self, record):
        url = reverse("forecasts:alert_level_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_description(self, record):
        link_html = '<a href="{}" class="btn btn-link p-0 text-decoration-none">{}</a>'
        url = reverse("forecasts:alert_level_entry", args=[record.id])
        return format_html(link_html, url, record.description)

    def render_delete(self, record):
        url = reverse("forecasts:alert_level_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class InstructionsTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Instructions", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": ""}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = DistrictForecastInstructions
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","description","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }
    
    def render_edit(self, record):
        url = reverse("forecasts:instructions_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_description(self, record):
        link_html = '<a href="{}" class="btn btn-link p-0 text-decoration-none">{}</a>'
        url = reverse("forecasts:instructions_entry", args=[record.id])
        return format_html(link_html, url, record.description)

    def render_delete(self, record):
        url = reverse("forecasts:instructions_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)

class RiskLevelTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Risk Alert Level", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    color = tables.Column(verbose_name="Color")
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

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
        url = reverse("forecasts:risk_level_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("forecasts:risk_level_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class SeverityTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Risk Alert Level", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    color = tables.Column(verbose_name="Color")
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = Severity
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
        url = reverse("forecasts:severity_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("forecasts:severity_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class ProbabilityTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:75px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:75px;","class": ""}, "td": {"style": "","class": ""}})
    description = tables.Column(verbose_name="Risk Alert Level", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    color = tables.Column(verbose_name="Color")
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:75px;","class": "col_edit"},"td": {"style": "","class": "col_delete"}})

    class Meta:
        model = Probability
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
        url = reverse("forecasts:probability_entry", args=[record.id])
        return format_html('<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>', url)
    
    def render_delete(self, record):
        url = reverse("forecasts:probability_delete", args=[record.id])
        return format_html('<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>', url)
    
class DistrictForecastTable(tables.Table):
    edit = tables.Column(empty_values=(), verbose_name="Edit",attrs={"th": {"style": "width:60px;","class": "text-center"}, "td": {"style": "","class": "col_edit text-center"}})
    
    forecast_date = tables.Column(verbose_name="Forecast Date", attrs={"th": {"style": "","class": ""}, "td": {"style": "","class": "col_link"}})
    pdf_file = tables.Column(empty_values=(),verbose_name="PDF",orderable=False,
        attrs={"th": {"style": "width:65px; text-align:center;","class": ""},"td": {"style": "text-align:center;","class": "col_pdf"}})
    created_datetime = tables.Column(verbose_name="Created Date", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "fst-italic;","class": ""}})
    updated_datetime = tables.Column(verbose_name="Updated Date", attrs={"th": {"style": "width:200px;","class": ""}, "td": {"style": "","class": ""}})
    
    is_published = tables.TemplateColumn(
        template_name="district-forecast/district_forecast_publish_toggle.html",
        verbose_name="Published",
        orderable=False,
        attrs={"th": {"style": "width:75px;","class": "text-center"},"td": {"style": "","class": "text-center"}})
    
    id = tables.Column(verbose_name="ID",attrs={"th": {"style": "width:100px;","class": "text-end"}, "td": {"style": "","class": "text-end"}})
    delete = tables.Column(empty_values=(), verbose_name="Delete",attrs={"th": {"style": "width:65px;","class": "text-center col_edit"},"td": {"style": "","class": "text-center col_delete"}})

    class Meta:
        model = DistrictForecast
        template_name = "django_tables2/bootstrap5.html"  # or bootstrap5
        fields = ("edit","forecast_date","created_datetime","updated_datetime","pdf_file","is_published","id","delete")

        # Add table HTML id and CSS classes here
        attrs = {
            "id": "table_pest_alert_level",           # unique table ID
            "class": "table table-striped table-condensed table-hover tbl_wimp3" # Bootstrap-friendly styling
        }

    def render_edit(self, record):
        link_html   = '<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>'
        url         = reverse("forecasts:district_forecast_details_entry", args=[record.id])
        return format_html(link_html, url, record.forecast_date.strftime("%B %d, %Y"))

    def render_forecast_date(self, record):
        link_html   = '<a href="{}" class="btn btn_edit_link p-0" disabled>{}</a>'
        url         = reverse("forecasts:district_forecast_details_entry",args=[record.id])
        return format_html(link_html, url, record.forecast_date.strftime("%B %d, %Y"))
    
    def render_pdf_file(self, record):
        link_html   = '<a href="{}" class="btn_pdf" target="_blank"><i class="fa-solid fa-file-pdf"></i></a>'
        url         = reverse("forecasts:generate_pdf", args=[record.id])  # change "pest_edit" to your URL name
        return format_html(link_html, url)
    
    def render_delete(self, record):
        link_html   = '<a href="{}" class="btn_delete"><i class="fa-solid fa-trash"></i></a>'
        url         = reverse("forecasts:district_forecast_delete", args=[record.id])
        return format_html(link_html, url)

class DistrictForecastDetailsTable(tables.Table):

    edit            = tables.Column(empty_values=(), verbose_name="Edit",attrs={
                        "th": {"style": "width:60px;","class": "col_edit text-center"},
                        "td": {"style": "","class": "col_edit text-center"}
                        })
    
    district         = tables.Column(verbose_name="District",attrs={
                        "th": {"style": "width:15%;","class": ""},
                        "td": {"style": "","class": "text-start text-decoration-none"}
                        })
    
    precip_max         = tables.Column(verbose_name="Precip (MAX)",attrs={
                        "th": {"style": "width:15%;","class": ""},
                        "td": {"style": "","class": "pe-4"}
                        })
    
    temp_max         = tables.Column(verbose_name="TEMP °F (MAX)",attrs={
                        "th": {"style": "width:15%;","class": ""},
                        "td": {"style": "","class": "pe-4"}
                        })
    temp_min         = tables.Column(verbose_name="TEMP °F (MIN)",attrs={
                        "th": {"style": "width:15%;","class": ""},
                        "td": {"style": "","class": "pe-4"}
                        })
    
    winds         = tables.Column(verbose_name="Winds (Kts)",empty_values=(),attrs={
                        "th": {"style": "width:15%;","class": ""},
                        "td": {"style": "","class": "pe-4"}
                        })
    
    weather_conditions = tables.Column(verbose_name="Weather Conditions",attrs={
                        "th": {"style": "","class": ""},
                        "td": {"style": "","class": ""}
                        })

    class Meta:
        model = DistrictForecastDetails
        template_name = "django_tables2/bootstrap4.html"  # or bootstrap5
        fields      = ("edit","district","temp_max","temp_min","precip_max","weather_conditions","id","forecast_id")
        sequence    = ("edit","district","weather_conditions","temp_max","temp_min","winds","precip_max")
        
        # Add table ID and class here
        attrs = {
            "id": "",
            "class": "tbl_wimp3 table table-striped table-condensed table-hover tbl_wimp3",
        }

    def render_edit(self, record):
        link_html   = '<a href="{}" class="btn_edit"><i class="fa-solid fa-pen-to-square"></i></a>'
        url         = reverse("forecasts:district_forecast_details_entry_item", args=[record.forecast_id, record.id,])
        return format_html(link_html, url, record.district)
    
    def render_district(self, record):
        link_html   = '<a href="{}" class="btn btn_edit_link p-0 text-decoration-none fw-bold">{}</a>'
        url         = reverse("forecasts:district_forecast_details_entry_item", args=[record.forecast_id, record.id,])
        return format_html(link_html, url, record.district)
    
    def render_temp_max(self, record):

        prob_class  = "bg-dark"
        sev_class   = "bg-dark"
        risk_class  = "bg-dark"

        if record.prob_temp_max:
            
            prob_text = str(record.prob_temp_max).lower()

            if "low" in prob_text:
                prob_class = "low"
            elif "medium" in prob_text:
                prob_class = "med text-dark"
            elif "high" in prob_text:
                prob_class = "high"

        if record.sev_temp_max:

            sev_text = str(record.sev_temp_max).lower()

            if "low" in sev_text:
                sev_class = "low"
            elif "medium" in sev_text:
                sev_class = "med text-dark"
            elif "high" in sev_text:
                sev_class = "high" 

        if record.risk_temp_max:

            risk_text = str(record.risk_temp_max).lower()

            if "low" in risk_text:
                risk_class = "low"
            elif "medium" in risk_text:
                risk_class = "med text-dark"
            elif "high" in risk_text:
                risk_class = "high"
            elif "critical" in risk_text:
                risk_class = "critical"

        link_html   = '<div class="fst-italic mb-1">{}</div><div class="row text-muted"><div class="col"><small>Probability:</small><br /><div class="badge {}">{}</div></div><div class="col"><small>Severity:</small><br /><div class="badge {}">{}</div></div><div class="col"><small>Risk:</small><br /><div class="badge {}">{}</div></div></div>'
        return format_html(link_html, record.temp_max, prob_class, record.prob_temp_max, sev_class, record.sev_temp_max, risk_class, record.risk_temp_max)
    
    def render_temp_min(self, record):

        prob_class  = "bg-dark"
        sev_class   = "bg-dark"
        risk_class  = "bg-dark"

        if record.prob_temp_min:
            
            prob_text = str(record.prob_temp_min).lower()

            if "low" in prob_text:
                prob_class = "low"
            elif "medium" in prob_text:
                prob_class = "med text-dark"
            elif "high" in prob_text:
                prob_class = "high"

        if record.sev_temp_min:
            
            sev_text = str(record.sev_temp_min).lower()

            if "low" in sev_text:
                sev_class = "low"
            elif "medium" in sev_text:
                sev_class = "med text-dark"
            elif "high" in sev_text:
                sev_class = "high"

        if record.risk_temp_min:
            
            risk_text = str(record.risk_temp_min).lower()

            if "low" in risk_text:
                risk_class = "low"
            elif "medium" in risk_text:
                risk_class = "med text-dark"
            elif "high" in risk_text:
                risk_class = "high"
            elif "critical" in risk_text:
                risk_class = "critical"

        link_html   = '<div class="fst-italic mb-1">{}</div><div class="row text-muted"><div class="col"><small>Probability:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Severity:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Risk:</small><br /><span class="badge {}">{}</span></div></div>'
        return format_html(link_html, record.temp_min, prob_class, record.prob_temp_min, sev_class, record.sev_temp_min, risk_class, record.risk_temp_min)
    
    def render_winds(self, record):

        prob_class  = "bg-dark"
        sev_class   = "bg-dark"
        risk_class  = "bg-dark"

        if record.prob_winds:
            
            prob_text = str(record.prob_winds).lower()

            if "low" in prob_text:
                prob_class = "low"
            elif "medium" in prob_text:
                prob_class = "med text-dark"
            elif "high" in prob_text:
                prob_class = "high"

        if record.sev_winds:
            
            sev_text = str(record.sev_winds).lower()

            if "low" in sev_text:
                sev_class = "low"
            elif "medium" in sev_text:
                sev_class = "med text-dark"
            elif "high" in sev_text:
                sev_class = "high"
            
        if record.risk_winds:
            
            risk_text = str(record.risk_winds).lower()

            if "low" in risk_text:
                risk_class = "low"
            elif "medium" in risk_text:
                risk_class = "med text-dark"
            elif "high" in risk_text:
                risk_class = "high"
            elif "critical" in risk_text:
                risk_class = "critical"

        link_html   = '<div class="fst-italic mb-1">{} - {}</div><div class="row text-muted"><div class="col"><small>Probability:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Severity:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Risk:</small><br /><span class="badge {}">{}</span></div></div>'
        return format_html(link_html, record.winds_min, record.winds_max, prob_class, record.prob_winds, sev_class, record.sev_winds, risk_class, record.risk_winds)
    
    def render_weather_conditions(self, record):

        prob_class = "bg-dark"
        sev_class = "bg-dark"
        risk_class = "bg-dark"

        prob_id = record.prob_weather_conditions_id
        sev_id = record.sev_weather_conditions_id

        ALERT_CLASSES = {
            1: "low", 2: "med text-dark", 3: "high",
        }

        if prob_id:
            prob_class = ALERT_CLASSES.get(prob_id, "bg-dark")

        if sev_id:
            sev_class = ALERT_CLASSES.get(sev_id, "bg-dark")
        
        RISK_MATRIX = {

            # PROBABILITY
            1: {  # LOW
                1: "low",
                2: "med text-dark",
                3: "med text-dark",
            },
            2: {  # MED
                1: "low",
                2: "med text-dark",
                3: "high",
            },
            3: {  # HIGH
                1: "low",
                2: "high",
                3: "critical"
            }
        }

        if prob_id and sev_id:
            risk_class = RISK_MATRIX.get(prob_id, {}).get(sev_id, "bg-dark")

        link_html   = '<div class="fst-italic mb-2">{}</div><div class="row text-muted"><div class="col"><small>Probability:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Severity:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Risk:</small><br /><span class="badge {}">{}</span></div></div>'
        return format_html(link_html, record.weather_conditions, prob_class, record.prob_weather_conditions, sev_class, record.sev_weather_conditions, risk_class, record.risk_weather_conditions)
    
    def render_precip_max(self, record):

        prob_class  = "bg-dark"
        sev_class   = "bg-dark"
        risk_class  = "bg-dark"

        if record.prob_precip_max:
            
            prob_text = str(record.prob_precip_max).lower()

            if "low" in prob_text:
                prob_class = "low"
            elif "medium" in prob_text:
                prob_class = "med text-dark"
            elif "high" in prob_text:
                prob_class = "high"
        
        if record.sev_precip_max:
            
            sev_text = str(record.sev_precip_max).lower()

            if "low" in sev_text:
                sev_class = "low"
            elif "medium" in sev_text:
                sev_class = "med text-dark"
            elif "high" in sev_text:
                sev_class = "high"
            
        if record.risk_precip_max:
            risk_text = str(record.risk_precip_max).lower()

            if "low" in risk_text:
                risk_class = "low"
            elif "medium" in risk_text:
                risk_class = "med text-dark"
            elif "high" in risk_text:
                risk_class = "high"
            elif "critical" in risk_text:
                risk_class = "critical"

        link_html   = '<div class="fst-italic mb-1">{}</div><div class="row text-muted"><div class="col"><small>Probability:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Severity:</small><br /><span class="badge {}">{}</span></div><div class="col"><small>Risk:</small><br /><div class="badge {}">{}</span></div></div>'
        return format_html(link_html, record.precip_max, prob_class, record.prob_precip_max, sev_class, record.sev_precip_max, risk_class, record.risk_precip_max)