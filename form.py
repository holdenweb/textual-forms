import wingdbstub

from typing import Dict, Any, Type, Optional, List, Callable

from field import Field, TextField, IntegerField, BooleanField, ChoiceField


from textual.app import App, ComposeResult

from textual.containers import Container, Vertical
from textual.message_pump import _MessagePumpMeta
from textual.widgets import Button

class FormMetaclass(_MessagePumpMeta):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields.update(base._declared_fields)
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        attrs['_declared_fields'] = fields
        return super().__new__(cls, name, bases, attrs)

class Form(Container, metaclass=FormMetaclass):
    def __init__(self, *children, field_order: Optional[List[str]] = None, **kwargs):
        super().__init__(*children, **kwargs)
        self.fields: Dict[str, Field] = {}
        self._populate_fields(field_order)

    def _populate_fields(self, field_order: Optional[List[str]] = None):
        if field_order:
            for name in field_order:
                if name in self._declared_fields:
                    self.fields[name] = self._declared_fields[name]
                    self.fields[name].name = name
                    self.fields[name].form = self
        else:
            for name, field in self._declared_fields.items():
                self.fields[name] = field
                field.name = name
                field.form = self

    async def on_mount(self) -> None:
        for field in self.fields.values():
            await self.mount(field.widget)

    def validate(self) -> Dict[str, List[str]]:
        errors: Dict[str, List[str]] = {}
        for name, field in self.fields.items():
            field_errors = field.run_validators(field.value)
            if field_errors:
                errors[name] = field_errors
        return errors

    def get_data(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for name, field in self.fields.items():
            data[name] = field.value
        return data

    def set_data(self, data: Dict[str, Any]):
        for name, value in data.items():
            if name in self.fields:
                self.fields[name].value = value
                self.fields[name].widget.value = self.fields[name].to_widget_value(value)

# Validator functions

from typing import Any, List

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


class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Vertical(MyForm(), Button("Submit"), id="form_container")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        form = self.query_one(MyForm)
        if form.validate():
            data = form.get_data()
            self.notify(f"Form data: {data}")
        else:
            self.notify("Form validation failed.")

if __name__ == "__main__":
    app = MyApp()
    app.run()