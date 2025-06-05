import  wingdbstub
# app.py
from textual import on
from textual_forms.validators import EvenInteger, Palindromic
from textual_forms.form import Form
from textual_forms.field import IntegerField, TextField, ChoiceField, BooleanField
from textual.app import App, ComposeResult
from textual.validation import Number
from textual.notifications import annotations

class MyForm(Form):
    name = TextField(
        placeholder="Name (palindrome)",
        required=True,
        validators=[Palindromic()],
        id="form-name",
    )
    age = IntegerField(
        placeholder="Age (must be even)",
        required=False,
        validators=[Number(minimum=0, maximum=130), EvenInteger()],
        id="form-age",
    )
    is_active = BooleanField(label="Active?", id="form-isactive")
    choice = ChoiceField(
        prompt="Select pill colo(u)r",
        choices=[("blue", "Blue"), ("red", "Red")],
        label="Selection",
        id="form-choice",
    )

def build_app(data=None):

    class MyApp(App):

        CSS_PATH = "app.tcss"
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.app_form = MyForm(data=data)  # simplify access for testing and debugging

        def compose(self) -> ComposeResult:
            yield self.app_form.render_form(id="form-container")

        @on(Form.Submitted)
        async def form_submitted(self, event: Form.Submitted) -> None:
            form = event.form
            data = form.get_data()
            self.notify(f"Form data: valid: {(await form.validate())}, {data}")

        @on(Form.Cancelled)
        async def form_cancelled(self, event: Form.Cancelled) -> None:
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