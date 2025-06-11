#import  wingdbstub

# form.py
import copy

from .field import Field

from typing import Dict, Any, Optional, List

from textual import on
from textual.containers import Vertical, Center, Horizontal
from textual.widgets import Button, Static
from textual.message import Message

from textual_forms.validators import EvenInteger, Palindromic

class FormMetaclass(type):
    """Collect Fields declared on the base classes."""
    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                # add each field to current_fields and remove as attribute
                current_fields.append((key, value))
                attrs.pop(key)
        _declared_fields = dict(current_fields)

        new_class = super().__new__(mcs, name, bases, attrs)

        new_class._base_fields = _declared_fields
        new_class._declared_fields = _declared_fields

        return new_class

class BaseForm:

    def __init__(self, *children, data: Optional[Dict[str, Any]] = None, field_order: Optional[List[str]] = None, **kwargs):
        self.data = data
        self.children = children
        self.field_order = field_order
        self.kwargs = kwargs
        self.fields: Dict[str, Field] = {}
        self._populate_fields(field_order)


        # THIS CHUNK FROM DJANGO
        # The _base_fields class attribute is the *class-wide* definition of
        # fields. Because a particular *instance* of the class might want to
        # alter self.fields, we create self.fields here by copying _base_fields.
        # Instances should always modify self.fields; they should not modify
        # self._base_fields.
        self.fields = copy.deepcopy(self._base_fields)
        self.order_fields(self.field_order)
        # THIS CHUNK FROM DJANGO ENDS

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

    def order_fields(self, field_order):
        """
        Rearrange the fields according to field_order.

        field_order is a list of field names specifying the order. Append fields
        not included in the list in the default order for backward compatibility
        with subclasses not overriding field_order. If field_order is None,
        keep all fields in the order defined in the class. Ignore unknown
        fields in field_order to allow disabling fields in form subclasses
        without redefining ordering.
        """
        if field_order is None:
            return
        fields = {}
        for key in field_order:
            try:
                fields[key] = self.fields.pop(key)
            except KeyError:  # ignore unknown fields
                pass
        for k in list(self.fields):
            fields[k] = self.fields.pop(k)
        assert not self.fields
        self.fields = fields

    def render_form(self, id):
        """
        Return a Vertical subclass with all the widgets inside it. The
        widgets are extracted from each field in turn and rendered inside the
        Vertical, followed by the buttons.

        XXX There's no way to specify the buttons, so there's just a submit
        for the present.
        """
        self.rform = RenderedForm(self, id=id, data=self.data, field_order=self.field_order)
        return self.rform


class Form(BaseForm, metaclass=FormMetaclass):
    "A collection of Fields, plus their associated data."
    # This is a separate class from BaseForm in order to abstract the way
    # self.fields is specified. This class (Form) is the one that does the
    # fancy metaclass stuff purely for the semantic sugar -- it allows one
    # to define a form using declarative syntax.
    # BaseForm itself has no way of designating self.fields.

    class Submitted(Message):
        def __init__(self, r_form):
            super().__init__()
            self.form = r_form

    class Cancelled(Message):
        def __init__(self, r_form):
            super().__init__()
            self.form = r_form


class RenderedForm(Vertical):

    DEFAULT_CSS = """
    Vertical {
    margin: 1;
    width: 1fr;
    height: auto;
    }
    StringInput, IntegerInput {
        padding: 0;
    }
    Static {
        width: auto;
    }
    Center {
        width: 1fr;
    }
    RenderedForm {
        keyline: heavy blue;
    }
    #buttons {
        height: auto;
        align: center middle;
    }
    TextWidget {
        height: 4;
    }
"""
    def __init__(self, form, data: Optional[Dict[str, Any]] = None, field_order: Optional[List[str]] = None, id=None):
        super().__init__(*form.children, id=id, **form.kwargs)
        self.form = form
        self.fields = form.fields
        self.data = data
        self.field_order = field_order
        for name, field in self.form.fields.items():
            field.widget = field.create_widget()
        if data is not None:
            self.set_data(data)

    def compose(self):
        for name, field in self.form.fields.items():
            yield Vertical(field.widget)
            if self.data and name in self.data:
                field.value = self.data[name]
        yield Vertical(
            Horizontal(
                Button("Cancel", id="cancel"),
                Button("Submit", id="submit"),
                id="buttons"
            ),
            id="outer-buttons"
        )

    def get_data(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        for name, field in self.form.fields.items():
            data[name] = field.value
        return data

    def set_data(self, data: Dict[str, Any]):
        for name, value in data.items():
            if name in self.form.fields:
                self.form.fields[name].widget.value = str(value)

    async def validate(self):
        result = True
        for name, field in self.fields.items():
            widget = field.widget
            container = widget.parent
            await container.remove_children(".erm")
            vr = widget.validate(widget.value)
            if not vr.is_valid:
                result = False
                for msg in vr.failure_descriptions:
                    container.mount(Center(Static(msg), classes="erm"))
        return result

    @on(Button.Pressed, "#submit")
    async def submit_pressed(self, event: Button.Pressed) -> None:
        r_form = self.app.query_one("#form-container")
        if await r_form.validate():
            self.post_message(Form.Submitted(self))
        else:
            self.app.notify("Please fix issues before submitting")

    @on(Button.Pressed, "#cancel")
    async def cancel_pressed(self, event: Button.Pressed) -> None:
        r_form = self.app.query_one("#form-container")
        self.post_message(Form.Cancelled(self))
