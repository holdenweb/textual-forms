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
        self.cleaned_data: Dict[str, Any] = {} # Add cleaned_data attribute
        self.form_errors: List[str] = [] # To store form-level errors

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

    def clean(self) -> Dict[str, Any]:
        """
        Override this method to perform form-level validation.
        This method is called by `_clean_form()` and should return the
        cleaned data as a dictionary or None if there are errors.
        If a ValidationError is raised, the error will be caught
        and added to the form's errors.
        """
        return self.get_data() # Default: return raw data

    def add_error(self, field_name: Optional[str], error: str) -> None:
        """
        Adds an error to the form or a specific field.

        Args:
            field_name: The name of the field to add the error to, or None for
                        a form-level error.
            error: The error message.
        """
        if field_name:
            if field_name not in self.fields:
                raise ValueError(f"Field '{field_name}' does not exist in this form.")
            # Assuming fields have a place to store errors (e.g., field.errors)
            # You might need to add an 'errors' attribute to the Field class
            # to make this work.
            # self.fields[field_name].errors.append(error)
            pass
        else:
            self.form_errors.append(error)

    def _clean_form(self) -> None:
        """
        Performs form-level cleaning and validation.
        This method is called internally during form processing.
        """
        try:
            cleaned_data = self.clean()
        except ValidationError as e:
            self.add_error(None, str(e)) # Convert ValidationError to string
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data

# Custom Exception for Validation Errors
class ValidationError(Exception):
    """
    Exception raised for validation errors.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


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


class MyApp(App):
    def compose(self) -> ComposeResult:
        with Form(Button("Submit"), id="form_container"):
            yield TextField(label="Name", required=True)
            yield IntegerField(label="Age", required=False,
                validators=[validate_even_number, validate_max_value(99)])
            yield BooleanField(label="Active")
            yield ChoiceField(choices=[("option1","Option 1"),("option2","Option 2")], label = "Selection")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        form = self.query_one(MyForm)
        form._clean_form() # Call form cleaning
        if not form.form_errors and not form.validate(): # Check for both field and form errors
            data = form.cleaned_data
            self.notify(f"Form data: {data}")
        else:
            self.notify("Form validation failed.")
            # Optionally, display form_errors and field errors

if __name__ == "__main__":
    app = MyApp()
    app.run()