from typing import List

from textual.widgets import Input, Checkbox, Select, Label
from textual.containers import Vertical

class TextFieldWidget(Input):
    def __init__(self, field: "Field", **kwargs):  # Forward reference
        super().__init__(**kwargs)
        self.field = field


class IntegerFieldWidget(Input):
    def __init__(self, field: "Field",  **kwargs): # Forward reference
        super().__init__(**kwargs)
        self.field = field


class BooleanFieldWidget(Checkbox):
    def __init__(self, field: "Field", **kwargs): # Forward reference
        super().__init__(**kwargs)
        self.field = field

    def field_default_value(self):
        return False


class ChoiceFieldWidget(Select):
    def __init__(self, field: "Field", choices: List[tuple[str, str]], **kwargs): # Forward reference
        super().__init__(options=choices, **kwargs)
        self.field = field

    def field_default_value(self):
        return Select.BLANK

