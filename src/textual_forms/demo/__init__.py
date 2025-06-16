# app.py
from textual import on
from textual_forms.form import Form
from textual.app import App, ComposeResult
from textual_forms.demo.testform import TestForm

def build_app(data=None, field_order=None, form=None):

    class MyApp(App):

        def __init__(self, data=data, field_order=field_order, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cancel_count = self.submit_count = 0
            self.app_form = form if form is not None else TestForm(data=data, field_order=field_order)  # simplifies access for testing and debugging
            self.data = data
            self.field_order = field_order

        def compose(self) -> ComposeResult:
            yield self.app_form.render(id="form-container")

        @on(Form.Submitted)
        async def form_submitted(self, event: Form.Submitted) -> None:
            form = event.form
            self.submit_count += 1
            data = form.get_data()
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