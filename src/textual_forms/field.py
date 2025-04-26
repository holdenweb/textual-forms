from typing import Any, Callable, List, Optional

from .widget import TextFieldWidget, IntegerFieldWidget, BooleanFieldWidget, ChoiceFieldWidget

class Field:

    def __init__(
        self,
        label: str = "",
        required: bool = True,
        validators: Optional[List[Callable[[Any], List[str]]]] = None,
        help_text: str = "",
        **kwargs,
    ):
        self.kwargs = kwargs
        self.label = label
        self.required = required
        self.validators = validators or []
        self.help_text = help_text
        self.name: str = ""
        self.form: Optional["Form"] = None  # Forward reference
        self.widget = self.create_widget()
        self.value: Any = self.field_default_value()
    def field_default_value(self) -> str:
        return ""

    def run_validators(self, value: Any) -> List[str]:
        errors: List[str] = []
        if self.required and value is None:
            errors.append(f"{self.label} is required.")
        if self.validators:
            for validator in self.validators:
                result = validator(value)
                if result:
                    errors.extend(result)
        return errors

    @property
    def value(self):
        return self.widget.value

    @value.setter
    def value(self, value):
        self.widget.value = value

    def to_python(self, value: Any) -> Any:
        return value

    def to_widget_value(self, value: Any) -> Any:
        return value

    def create_widget(self):
        raise NotImplementedError("Subclasses must implement create_widget()")

class TextField(Field):
    def create_widget(self):
        return TextFieldWidget(field = self, **self.kwargs)

class IntegerField(Field):
    def create_widget(self):
        return IntegerFieldWidget(field = self, **self.kwargs)

    def to_python(self, value: str) -> Optional[int]:
        try:
            return int(value)
        except ValueError:
            return None

class BooleanField(Field):
    def create_widget(self):
        return BooleanFieldWidget(field = self, **self.kwargs)

    def to_python(self, value: bool) -> bool:
        return value

class ChoiceField(Field):

    def __init__(
        self,
        choices: List[tuple[str, str]],
        label: str = "",
        required: bool = True,
        validators: Optional[List[Callable[[Any], List[str]]]] = None,
        help_text: str = "",
        **kwargs,
    ):
        self.choices = choices
        self.kwargs = kwargs
        super().__init__(label, required, validators, help_text)

    def field_default_value(self):
        return self.widget.field_default_value(**self.kwargs)

    def create_widget(self):
        return ChoiceFieldWidget(field=self, choices=self.choices, **self.kwargs)

    def to_python(self, value: str) -> str:
        return value