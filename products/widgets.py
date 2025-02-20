from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """ Custom Clearable File Input Widget """

    clear_checkbox_label = _('Remove this image?')
    initial_text = _('Image currently in use:')
    input_text = _('')
    template_name = (
        'products/custom_widget_templates/custom_clearable_file_input.html')
