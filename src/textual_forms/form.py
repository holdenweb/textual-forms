import copy

from .field import Field

from typing import Dict, Any, Optional, List

from textual.containers import Vertical
from textual.message_pump import _MessagePumpMeta

class FormMetaclass(_MessagePumpMeta):
    """Collect Fields declared on the base classes."""
    def __new__(mcs, name, bases, attrs):
        # Collect fields from current class.
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                # add each field to current_fields and remove as attribute
                current_fields.append((key, value))
                attrs.pop(key)
        declared_fields = dict(current_fields)

        new_class = super().__new__(mcs, name, bases, attrs)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class

class BaseForm:
    def __init__(self, *children, field_order: Optional[List[str]] = None, **kwargs):
        self.children = children
        self.field_order = field_order
        self.kwargs = kwargs
        self.fields: Dict[str, Field] = {}
        self._populate_fields(field_order)


        # THIS CHUNK FROM DJANGO
        # The base_fields class attribute is the *class-wide* definition of
        # fields. Because a particular *instance* of the class might want to
        # alter self.fields, we create self.fields here by copying base_fields.
        # Instances should always modify self.fields; they should not modify
        # self.base_fields.
        self.fields = copy.deepcopy(self.base_fields)
        self._bound_fields_cache = {}
        self.order_fields(self.field_order if field_order is None else field_order)
        # THIS CHUNK FROM DJANGO ENDS

    def _populate_fields(self, field_order: Optional[List[str]] = None):
        if field_order:
            for name in field_order:
                if name in self._declared_fields:
                    self.fields[name] = self._declared_fields[name]
                    self.fields[name].name = name
                    self.fields[name].form = self
        else:
            for name, field in self.declared_fields.items():
                self.fields[name] = field
                field.name = name
                field.form = self

    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self.add_error(name, e)

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
        fields.update(self.fields)  # add remaining fields in original order
        self.fields = fields

    def render_form(self, id):
        """
        Return a Vertical subclass with all the widgets inside it. The
        widgets are extracted from each field in turn and rendered inside the
        Vertical, followed by the buttons.

        XXX There's no way to specify the buttons, so there's just a submit
        for the present.
        """
        self.rform = RenderedForm(self, id=id)
        return self.rform


class Form(BaseForm, metaclass=FormMetaclass):
    "A collection of Fields, plus their associated data."
    # This is a separate class from BaseForm in order to abstract the way
    # self.fields is specified. This class (Form) is the one that does the
    # fancy metaclass stuff purely for the semantic sugar -- it allows one
    # to define a form using declarative syntax.
    # BaseForm itself has no way of designating self.fields.


class RenderedForm(Vertical):

    def __init__(self, form, id=None):
        super().__init__(*form.children, id=id, **form.kwargs)
        self.form = form
        self.fields = form.fields

    async def on_mount(self) -> None:
        for field in self.form.fields.values():
            await self.mount(Vertical(field.widget))

    def validate(self) -> Dict[str, List[str]]:
        form = self.form
        errors: Dict[str, List[str]] = {}
        for name, field in form.fields.items():
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
