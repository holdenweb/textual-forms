import wingdbstub

from textual_forms.app import build_app
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
