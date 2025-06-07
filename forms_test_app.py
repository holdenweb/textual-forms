from textual import on
from textual_forms.form import RenderedForm, Form
from textual_forms.field import IntegerField, StringField, ChoiceField, BooleanField
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Vertical
from textual.validation import Number, Integer
from typing import Any, List

from testform import TestForm


def build_app(data=None, field_order=None):

    class MyApp(App):

        CSS_PATH = "forms_test_app.tcss"

        def __init__(self, data=None, field_order=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cancel_count = self.submit_count = 0
            self.app_form = TestForm(data=data, field_order=field_order)  # simplify access for testing and debugging

        def compose(self) -> ComposeResult:
            yield self.app_form.render_form(id="form-container")

        @on(Form.Submitted)
        async def form_submitted(self, event: Form.Submitted) -> None:
            self.submit_count += 1
            self.notify("Submitted")

        @on(Form.Cancelled)
        async def form_cancelled(self, event: Form.Cancelled) -> None:
            self.cancel_count += 1
            self.notify("Cancelled")

        def on_click(self, e):
            self.log(self.tree)
            self.log(self.css_tree)


    return MyApp(data=data, field_order=field_order)

if __name__ == "__main__":
    app = build_app()
    app.run()