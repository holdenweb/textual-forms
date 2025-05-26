import wingdbstub

from textual_forms.app import MyApp
import pytest
import pytest_asyncio

@pytest.fixture()
def app():
    yield MyApp()

@pytest_asyncio.fixture()
async def pilot(app):
    async with app.run_test() as p:
        yield p

@pytest.mark.asyncio
async def test_text_field(app):
    async with app.run_test() as pilot:
        name_widget = app.query_one("#form-name")
        name_widget.focus()
        for c in "Steve Holden":
            await pilot.press(c)
        assert name_widget.value == "Steve Holden"


@pytest.mark.asyncio
async def test_choice_field(app):
    async with app.run_test() as pilot:
        choice_widget = app.query_one("#form-isactive")
        choice_widget.focus()
        v = choice_widget.value
        await pilot.press(" ")
        assert choice_widget.value == (not v)


@pytest.mark.asyncio
async def test_integer_field(app):
    async with app.run_test() as pilot:
        age_widget = app.query_one("#form-age")
        age_widget.focus()
        for c in "120":
            await pilot.press(c)
        v = age_widget.value
        assert v == '120'
        assert age_widget.field.value == 120


@pytest.mark.asyncio
async def test_rendered_form(app, pilot):
    fields = app.app_form.rform.fields
    assert list(fields) == ["name", "age", "is_active", "choice"]

@pytest.mark.asyncio
async def test_x(pilot):
    assert pilot is not None
