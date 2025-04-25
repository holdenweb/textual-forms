from .field import Field

from typing import Dict, Any, Optional, List

from textual.containers import Vertical
from textual.message_pump import _MessagePumpMeta

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

class Form(metaclass=FormMetaclass):
    def __init__(self, *children, field_order: Optional[List[str]] = None, **kwargs):
        self.children = children
        self.kwargs = kwargs
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


    def render(self):
        """
        Return a Vertical subclass with all the widgets inside it. The
        widgets are extracted from each field in turn and rendered inside the
        Vertical, followed by the buttons.

        XXX There's no way to specify the buttons, so there's just a submit
        for the present.
        """
        class RenderedForm(Vertical):

            def __init__(self, form, **kwargs):
                super().__init__(*form.children, **form.kwargs)
                self.form = form

            async def on_mount(self) -> None:
                for field in self.form.fields.values():
                    await self.mount(field.widget)

            def validate(self) -> Dict[str, List[str]]:
                errors: Dict[str, List[str]] = {}
                for name, field in self.form.fields.items():
                    field_errors = field.run_validators(field.value)
                    if field_errors:
                        errors[name] = field_errors
                return errors

            def get_data(self) -> Dict[str, Any]:
                data: Dict[str, Any] = {}
                for name, field in self.form.fields.items():
                    data[name] = field.value
                return data

            def set_data(self, data: Dict[str, Any]):
                for name, value in data.items():
                    if name in self.form.fields:
                        self.form.fields[name].value = value
                        self.form.fields[name].widget.value = self.form.fields[name].to_widget_value(value)

        return RenderedForm(self, id="first-form")
