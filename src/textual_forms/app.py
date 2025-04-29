import wingdbstub

from .form import Form
from .field import IntegerField, TextField, ChoiceField, BooleanField
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.validation import Number, Validator, ValidationResult
# Validator functions


class EvenInteger(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            value = int(value)
        except ValueError:
            return self.failure("Not an integer")
        if value % 2:
            return self.failure("Odd number")
        else:
            return self.success()


class MyForm(Form):

    name = TextField(label="Name", required=True, id="form-name")
    age = IntegerField(label="Age", required=False,
        validators=[Number(minimum=0, maximum=130), EvenInteger()], id="form-age")
    is_active = BooleanField(label="Active", id="form-isactive")
    choice = ChoiceField(choices=[("option1","Option 1"),("option2","Option 2")], label = "Selection", id='form-choice')

class MyApp(App):

    def __init__(self, *args, **kwargs):
        self.app_form = MyForm()  # simplify access for testing and debugging
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield self.app_form.render_form(id="form-container")
        yield Button("Submit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.log(self.app.tree)
        form = self.app.query_one("#form-container")
        if form.validate():
            data = form.get_data()
            self.notify(f"Form data: {data}")
        else:
            # LOGIC BELOW ACCESSES ERROR MESSAGES BY FIELD NAME
            #for vr in errors['age']:
                #for fd in vr.failure_descriptions: print(fd)
            self.notify("Form validation failed.")

def main():
    app = MyApp()
    app.run()

if __name__ == "__main__":
    main()