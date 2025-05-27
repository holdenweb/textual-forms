# app.py
from textual import on
from textual_forms.validators import EvenInteger, Palindromic
from textual_forms.form import Form
from textual_forms.field import IntegerField, TextField, ChoiceField, BooleanField
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.validation import Number

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
        choices=[("blue", "Option 1"), ("red", "Option 2")],
        label="Selection",
        id="form-choice",
    )

class MyApp(App):

    CSS_PATH = "app.tcss"
    def __init__(self, *args, **kwargs):
        self.app_form = MyForm()  # simplify access for testing and debugging
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield self.app_form.render_form(id="form-container")

    @on(Form.Submitted)
    def form_submitted(self, event: Form.Submitted) -> None:
        #if form.validate():
        form = event.form
        data = form.get_data()
        self.notify(f"Form data: {data}")
        self.app.log(self.app.tree)


def main():
    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()