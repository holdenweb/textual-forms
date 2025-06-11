# app.py
from textual import on
from textual_forms.validators import EvenInteger, Palindromic
from textual_forms.form import Form
from textual.app import App, ComposeResult
from textual.notifications import annotations
from textual_forms.demo.testform import TestForm

def build_app(data=None, field_order=None):

    class MyApp(App):

        def __init__(self, data=data, field_order=field_order, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cancel_count = self.submit_count = 0
            self.app_form = TestForm(data=data, field_order=field_order)  # simplifies access for testing and debugging
            self.data = data
            self.field_order = field_order

        def compose(self) -> ComposeResult:
            yield self.app_form.render_form(id="form-container")

        @on(Form.Submitted)
        async def form_submitted(self, event: Form.Submitted) -> None:
            form = event.form
            data = form.get_data()
            self.submit_count += 1
            self.notify(f"Form data: valid: {(await form.validate())}, {data}")

        @on(Form.Cancelled)
        async def form_cancelled(self, event: Form.Cancelled) -> None:
            self.cancel_count += 1
            self.notify("Cancelled")

        def on_click(self, e):
            self.log(self.tree)
            self.log(self.css_tree)

    return MyApp()

def main():
    app = build_app(data=None)
    app.run()

if __name__ == "__main__":
    main()