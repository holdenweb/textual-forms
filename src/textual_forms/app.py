from textual_forms.form import Form
from textual_forms.field import IntegerField, TextField, ChoiceField, BooleanField
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.validation import Number, Validator, ValidationResult


class EvenInteger(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            value = int(value)
        except ValueError:
            return self.success()  # Handled by other validators
        if value % 2:
            return self.failure("Not an even number")
        else:
            return self.success()

class Palindromic(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value == value[::-1]:
            return self.success()
        else:
            return self.failure("Not palindromic")


class MyForm(Form):
    name = TextField(placeholder="Name (palindrome)", required=True, validators=[Palindromic()], id="form-name")
    age = IntegerField(placeholder="Age (must be even)", required=False,
        validators=[Number(minimum=0, maximum=130), EvenInteger()], id="form-age")
    is_active = BooleanField(id="form-isactive")
    choice = ChoiceField(choices=[("option1","Option 1"),("option2","Option 2")], label = "Selection", id='form-choice')

class MyApp(App):

    CSS_PATH = "app.tcss"
    def __init__(self, *args, **kwargs):
        self.app_form = MyForm()  # simplify access for testing and debugging
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield self.app_form.render_form(id="form-container")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.log(self.app.tree)
        form = self.app.query_one("#form-container")
        #if form.validate():
        data = form.get_data()
        self.notify(f"Form data: {data}")

    def on_click(self, e):
        self.log(self.tree)

def main():
    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()