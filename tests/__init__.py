import pytest

from textual.app import App
from textual_forms.form import Form
from textual_forms.field import Field

def one_field_app(p_field):

    class OneFieldForm(Form):
        field = p_field

    class OneFieldApp(App):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.form = OneFieldForm()

        def compose(self):
            yield self.form.render(id="form-container")

    return OneFieldApp
