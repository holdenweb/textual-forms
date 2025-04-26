from typing import List

from textual.widgets import Input, Checkbox, Select, Label
from textual.containers import Vertical

class TextFieldWidget(Vertical):
    def __init__(self, field: "Field", **kwargs):  # Forward reference
        super().__init__(**kwargs)
        self.field = field
        self.input = Input(placeholder=self.field.label, **kwargs)

    def compose(self):
        yield self.input
        if self.field.run_validators(self.input.value):
            yield Label("\n".join(self.field.run_validators(self.input.value)), style="red")

    @property
    def value(self):
        return self.input.value

    @value.setter
    def value(self, new_value):
        self.input.value = new_value

class IntegerFieldWidget(Vertical):
    def __init__(self, field: "Field",  **kwargs): # Forward reference
        super().__init__()
        self.field = field
        self.input = Input(placeholder=self.field.label, type="number", **kwargs)

    def compose(self):
        yield self.input

    @property
    def value(self):
        return self.input.value

    @value.setter
    def value(self, new_value):
        self.input.value = new_value

class BooleanFieldWidget(Vertical):
    def __init__(self, field: "Field", **kwargs): # Forward reference
        super().__init__(**kwargs)
        self.field = field
        self.checkbox = Checkbox(self.field.label)

    def compose(self):
        yield self.checkbox

    @property
    def value(self):
        return self.checkbox.value

    @value.setter
    def value(self, new_value):
        self.checkbox.value = new_value

class ChoiceFieldWidget(Vertical):
    def __init__(self, field: "Field", choices: List[tuple[str, str]], **kwargs): # Forward reference
        super().__init__(**kwargs)
        self.field = field
        self.select = Select(options=choices, prompt=self.field.label)

    def field_default_value(self):
        return Select.BLANK

    def compose(self):
        yield self.select

    @property
    def value(self):
        return self.select.value

    @value.setter
    def value(self, new_value):
        self.select.value = new_value


