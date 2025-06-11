from textual_forms.field import IntegerField, StringField, ChoiceField, BooleanField, TextField
from textual_forms.form import Form
from textual_forms.validators import EvenInteger, Palindromic
from textual.validation import Number


class TestForm(Form):
    name = StringField(
        placeholder="Name (palindrome)",
        required=True,
        validators=[Palindromic()],
        id="form-name",
    )
    age = IntegerField(
        placeholder="Age (must be even)",
        required=False,
        validators=[Number(minimum=0, maximum=130), EvenInteger()],
        id="form-age",
    )
    description = TextField(
        required=True,
        id="form-description",
        text="This is a multi-line TextField",
    )

    is_active = BooleanField(label="Active?", id="form-isactive")

    choice = ChoiceField(
        prompt="Select pill colo(u)r",
        choices=[("blue", "Blue"), ("red", "Red")],
        label="Selection",
        id="form-choice",
        required=True,
    )