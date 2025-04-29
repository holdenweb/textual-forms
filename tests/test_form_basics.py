import wingdbstub

from textual_forms.app import MyApp
import pytest
@pytest.fixture(scope='function')
def app():
    yield MyApp()

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
        assert age_widget.field.to_python(v) == 120


