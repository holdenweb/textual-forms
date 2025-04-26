from textual_forms.app import MyApp
import pytest
@pytest.fixture(scope='function')
def app():
    yield MyApp()

@pytest.mark.asyncio
async def test_app_creation(app):
    async with app.run_test() as pilot:
        for c in "Steve Holden":
            await pilot.press(c)
        assert app.query_one("#form-name").value == "Steve Holden"
        await pilot.press("ctrl+q")  # Terminate app
