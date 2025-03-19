from typing import Any, Callable, List, Optional, Union
from textual.widgets import Input, Checkbox, Select

class Field:
    def __init__(self, label: str = "", required: bool = True, validators: Optional[List[Callable[[Any], bool]]] = None, help_text: str = ""):
        self.label = label
        self.required = required
        self.validators = validators or []
        self.help_text = help_text
        self.value: Any = None
        self.name: str = ""
        self.form: Optional[Form] = None
        self.widget = self.create_widget()

    def create_widget(self):
        raise NotImplementedError("Subclasses must implement create_widget()")

    def validate(self) -> bool:
        """Validates the field's value."""
        if self.required and self.value is None:
            return False
        for validator in self.validators:
            if not validator(self.value):
                return False
        return True

    def to_python(self, value: Any) -> Any:
        """Converts the widget value to a Python type."""
        return value

    def to_widget_value(self, value: Any) -> Any:
        """Converts the python value to a widget value"""
        return value

class TextField(Field):
    def create_widget(self):
        return Input(placeholder=self.label)

    def to_python(self, value: str) -> str:
        return value

class IntegerField(Field):
    def create_widget(self):
        return Input(placeholder=self.label, type="number")

    def to_python(self, value: str) -> Optional[int]:
        try:
            return int(value)
        except ValueError:
            return None

class BooleanField(Field):
    def create_widget(self):
        return Checkbox(self.label)

    def to_python(self, value: bool) -> bool:
        return value

    def to_widget_value(self, value: bool) -> bool:
        return value

class ChoiceField(Field):
    def __init__(self, choices: List[Union[str, tuple[str, str]]], label: str = "", required: bool = True, validators: Optional[List[Callable[[Any], bool]]] = None, help_text: str = ""):
        self.choices = choices
        super().__init__(label, required, validators, help_text)

    def create_widget(self):
        options = []
        for choice in self.choices:
            if isinstance(choice, tuple):
                options.append(choice)
            else:
                options.append((choice, choice))
        return Select(options=options, prompt=self.label)

    def to_python(self, value: str) -> str:
        return value

    def to_widget_value(self, value: str) -> str:
        return value