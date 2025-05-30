import wingdbstub

from textual_forms.form import RenderedForm, Form
from textual_forms.field import IntegerField, TextField, ChoiceField, BooleanField
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Vertical

from typing import Any, List

from textual_forms.validators import EvenInteger, Palindromic


class MyForm(Form):

    name = TextField(label="Name", validators=[Palindromic()], required=True)
    age = IntegerField(label="Age", required=False,
        validators=[EvenInteger()])
    is_active = BooleanField(label="Active")
    choice = ChoiceField(choices=[("red","Red"),("blue","Blue")], label = "Pill colour")

def build_app(data=None, field_order=None):

    class MyApp(App):

        CSS_PATH = "form_test_app.tcss"

        def __init__(self, data=None, field_order=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.app_form = MyForm(data=data, field_order=field_order)  # simplify access for testing and debugging

        def compose(self) -> ComposeResult:
            yield self.app_form.render_form(id="form-container")


        def on_button_pressed(self, event: Button.Pressed) -> None:
            form = self.query_one(RenderedForm)
            #if form.validate():
            data = form.get_data()
            self.notify(f"Form data: {data}")
            #else:
                #self.notify("Form validation failed.")

    return MyApp(data=data, field_order=field_order)

if __name__ == "__main__":
    app = build_app()
    app.run()