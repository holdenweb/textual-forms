from forms_test_app import build_app
import pytest
import pytest_asyncio

from textual.widgets import Button

@pytest.mark.asyncio(loop_scope="function")
async def test_data_injection():
    my_data = dict(name="anna", age=100, is_active=True, choice='Blue')
    app = build_app(data=my_data)
    async with app.run_test() as p:
        await p.click(Button)
        form = app.query_one("#form-container")
        assert form.get_data() == my_data

@pytest.mark.asyncio(loop_scope="function")
async def test_field_order():
    fo =  ["age", "is_active", ]
    my_data = dict(name="anna", age=100, is_active=True, choice='Blue')
    app = build_app(data=my_data, field_order=fo)
    async with app.run_test() as p:
        await p.click("#submit")
        form = app.query_one("#form-container")
        assert form.get_data() == my_data
        assert list(form.get_data()) == fo + ["name", "choice"]

