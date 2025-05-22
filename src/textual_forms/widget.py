from typing import List

from textual import on
from textual.widgets import Input, Checkbox, Select, Static, Label
from textual.containers import Center
from textual.events import Blur


def ids():
    count = 0
    while True:
        count += 1
        yield f"id-{count}"

ids = ids()


class FieldWidget:
    """
    Mixin to provide requirements for forms support.
    """
    async def on_input_changed(self, e):
        container = self.parent
        await container.remove_children(".erm")
        if (vr := e.validation_result) is not None and vr.is_valid:
            for msg in vr.failure_descriptions:
                container.mount(Center(Static(msg), classes="erm"))

    def errors(self):
        if not hasattr(self, '_errors') :
            # Field was never focused: validate to build _errors
            self._errors = self.validate()
        return self._errors


class TextWidget(Input, FieldWidget):
    def __init__(self, field: "Field", **kwargs):  # Forward reference
        super().__init__(**kwargs)
        self.field = field


class IntegerWidget(Input, FieldWidget):
    def __init__(self, field: "Field",  **kwargs): # Forward reference
        super().__init__(type='integer', **kwargs)
        self.field = field


class BooleanWidget(Checkbox, FieldWidget):
    def __init__(self, field: "Field", **kwargs): # Forward reference
        super().__init__(**kwargs)
        self.field = field

    def field_default_value(self):
        return False


class ChoiceWidget(Select, FieldWidget):
    def __init__(self, field: "Field", choices: List[tuple[str, str]], **kwargs): # Forward reference
        super().__init__(options=choices, **kwargs)
        self.field = field

    def field_default_value(self):
        return Select.BLANK

