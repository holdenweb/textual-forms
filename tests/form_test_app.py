from form import Form
from field import IntegerField, TextField, ChoiceField, BooleanField
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Vertical


from typing import Any, List

from textual.app import App, ComposeResult
from textual.widgets import Button

def validate_even_number(value: Any) -> List[str]:
    """
    Validates that the input is an even number.

    Args:
        value: The value to validate.

    Returns:
        A list of error messages. If the list is empty, the validation succeeded.
    """
    errors: List[str] = []
    if value is not None:
        if isinstance(value, int):
            if value % 2 != 0:
                errors.append("Value must be an even number.")
        else:
            errors.append("Value must be an integer.") # Or perhaps, "Invalid input type"
    return errors

def validate_max_value(max_value: int):
    """
    Returns a validator that checks if the input does not exceed max_value.
    """
    def validator(value: Any) -> List[str]:
        errors: List[str] = []
        if value is not None:
            if isinstance(value, int):
                if value > max_value:
                    errors.append(f"Value cannot exceed {max_value}.")
            else:
                errors.append("Value must be an integer.")
        return errors

    return validator

class MyForm(Form):

    name = TextField(label="Name", required=True)
    age = IntegerField(label="Age", required=False,
        validators=[validate_even_number, validate_max_value(99)])
    is_active = BooleanField(label="Active")
    choice = ChoiceField(choices=[("option1","Option 1"),("option2","Option 2")], label = "Selection")

def build_app(data=None, field_order=None):

    class MyApp(App):

        CSS_PATH = "app.tcss"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.app_form = MyForm(data=data, field_order=field_order)  # simplify access for testing and debugging

        def compose(self) -> ComposeResult:
            yield Vertical(MyForm(), Button("Submit"), id="form_container")

        def on_button_pressed(self, event: Button.Pressed) -> None:
            form = self.query_one(MyForm)
            if form.validate():
                data = form.get_data()
                self.notify(f"Form data: {data}")
            else:
                self.notify("Form validation failed.")

    return MyApp(data=None, field_order=None)

if __name__ == "__main__":
    app = build_app()
    app.run()