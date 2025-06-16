from textual_forms.demo import build_app
from textual_forms import StringField

from . import one_field_app

import pytest

@pytest.mark.asyncio(loop_scope="function")
async def test_typed_input():
    field = StringField(id="sf")
    app = one_field_app(field)()
    async with app.run_test() as pilot:
        test_field = app.query_one("#sf")
        for c in "Steve Holden":
            await pilot.press(c)
        assert test_field.value == "Steve Holden"


#@pytest.mark.asyncio(loop_scope="function")
#async def test_required():
    #field = StringField(id="sf", required=False)
    #app = one_field_app(field)()
    #async with app.run_test() as pilot:
        #test_field = app.query_one("#sf")
        #assert test_field.value == ""
        #assert not await app.form.validate()

