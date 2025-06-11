from textual_forms.demo import build_app
import pytest
import pytest_asyncio

from textual.widgets import Button

@pytest.mark.asyncio(loop_scope="function")
async def test_data_injection():
    my_data = dict(name="anna", age=100, is_active=True, choice='Blue', description="Nobody!")
    app = build_app(data=my_data)
    async with app.run_test(size=(80, 30)) as p:
        await p.click("#submit")
        form = app.query_one("#form-container")
        assert form.get_data() == my_data

@pytest.mark.asyncio(loop_scope="function")
async def test_field_order():
    fo =  ["age", "is_active", ]
    my_data = dict(name="anna", age=100, is_active=True, choice='Blue', description="Nobody2!")
    app = build_app(data=my_data, field_order=fo)
    async with app.run_test(size=(80, 30)) as p:
        await p.click("#submit")
        form = app.query_one("#form-container")
        assert form.get_data() == my_data
        assert list(app.app_form.fields) == fo + ["name", "description", "choice"]

