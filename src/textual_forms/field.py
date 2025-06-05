# field.py
from typing import Any, Callable, List, Optional

from .widget import StringWidget, IntegerWidget, BooleanWidget, ChoiceWidget

class Field:

    def __init__(
        self,
        label: str = "",
        required: bool = True,
        validators: Optional[List[Callable[[Any], List[str]]]] = None,
        help_text: str = "",
        disabled=False,
        widget=None,
        **kwargs,
    ):
        self.kwargs = kwargs
        self.label = label
        self.required = required
        self.validators = validators or []
        self.help_text = help_text
        self.name: str = ""
        self.form: Optional["Form"] = None
        self.disabled = disabled
        self.widget = widget

    @property
    def value(self):
        return self.widget.value

    @value.setter
    def value(self, value):  # Doesn't work for non-strring fields (esp. BooleanWidget)
        self.widget.value = str(value)

    def to_widget_value(self, value: Any) -> Any:
        return value

    def create_widget(self):
        if self.widget is None:
            raise NotImplementedError("Fields with no default widget must implement create_widget()")


class StringField(Field):
    def create_widget(self):
        return StringWidget(field=self, validators=self.validators, **self.kwargs)

class IntegerField(Field):
    def create_widget(self):
        return IntegerWidget(field=self, validators=self.validators, **self.kwargs)

    @property
    def value(self) -> Optional[int]:
        try:
            return int(self.widget.value)
        except ValueError:
            return None

    @value.setter
    def value(self, value):
        self.widget.value = str(value)

class BooleanField(Field):
    def create_widget(self):
        return BooleanWidget(field=self, label=self.label, **self.kwargs)

    def to_python(self, value: bool) -> bool:
        return value

    @property
    def value(self):
        #return {'True': True, 'False': False}[self.widget.value]
        return self.widget.value

    @value.setter
    def value(self, value):  # Doesn't work for non-string fields (esp. BooleanWidget)
        self.widget.value = value

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
        super().__init__(label, required, validators, help_text, **kwargs)

    def create_widget(self):
        return ChoiceWidget(field=self, choices=self.choices, **self.kwargs)

    def to_python(self, value: str) -> str:
        return value