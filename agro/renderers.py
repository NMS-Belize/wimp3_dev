from rest_framework.renderers import BrowsableAPIRenderer

class NoHTMLFormBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_rendered_html_form(self, *args, **kwargs):
        """We don't want the HTML forms to be rendered"""
        return ""
    
class NoDeleteBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['display_edit_forms'] = False # This can control all edit forms
        # Alternatively, to specifically disable the DELETE *button* from rendering in the top navigation, you can
        # manipulate how the context is set up depending on the DRF version, but modifying http_method_names is more reliable.
        return context
