from textual_forms.app import build_app
from textual_forms.form import RenderedForm

import pytest
import pytest_asyncio

@pytest_asyncio.fixture(loop_scope="function")
def app():
    # Fine when not providing data ...
    yield build_app()

@pytest_asyncio.fixture(loop_scope="function")
async def pilot(app):
    async with app.run_test() as p:
        yield p

@pytest.mark.asyncio(loop_scope="function")
async def test_text_field(app, pilot):
    name_widget = app.query_one("#form-name")
    name_widget.focus()
    for c in "Steve Holden":
        await pilot.press(c)
    assert name_widget.value == "Steve Holden"


@pytest.mark.asyncio(loop_scope="function")
async def test_choice_field(app, pilot):
    choice_widget = app.query_one("#form-isactive")
    choice_widget.focus()
    v = choice_widget.value
    await pilot.press(" ")
    assert choice_widget.value == (not v)


@pytest.mark.asyncio(loop_scope="function")
async def test_integer_field(app, pilot):
    age_widget = app.query_one("#form-age")
    age_widget.focus()
    for c in "120":
        await pilot.press(c)
    v = age_widget.value
    assert v == '120'
    assert age_widget.field.value == 120


@pytest.mark.asyncio(loop_scope="function")
async def test_fields_present(app, pilot):
    fields = app.app_form.rform.fields
    # Use a list because ordering should be  maintained
    assert list(fields) == ["name", "age", "is_active", "choice"]

@pytest.mark.asyncio(loop_scope="function")
async def test_validation(app, pilot):
    form = app.app_form.rform
    form.set_data(dict(name="anna", age=34, is_active=False, pill_choice='Blue'))
    assert await form.validate()
    form.set_data({"age": 1331})
    assert not await form.validate()