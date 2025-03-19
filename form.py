from textual.containers import Container
from typing import Dict, Any, Type, Optional
from field import Field

class Form(Container):
    def __init__(self, *children, **kwargs):
        super().__init__(*children, **kwargs)
        self.fields: Dict[str, Field] = {}
        self._populate_fields()

    def _populate_fields(self):
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                self.fields[name] = field
                field.name = name
                field.form = self

    async def on_mount(self) -> None:
        for field in self.fields.values():
            await self.mount(field.widget)

    def validate(self) -> bool:
        """Validates all fields in the form."""
        is_valid = True
        for field in self.fields.values():
            if not field.validate():
                is_valid = False
        return is_valid

    def get_data(self) -> Dict[str, Any]:
        """Returns the data from the form as a dictionary."""
        data: Dict[str, Any] = {}
        for name, field in self.fields.items():
            data[name] = field.value
        return data

    def set_data(self, data: Dict[str, Any]):
        """Sets the data for the form from a dictionary."""
        for name, value in data.items():
            if name in self.fields:
                self.fields[name].value = value
                self.fields[name].widget.value = self.fields[name].to_widget_value(value)