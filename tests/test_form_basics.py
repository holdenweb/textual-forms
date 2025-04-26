import sys
for p in sys.path:
    print(p)


import wingdbstub
from textual_forms.app import MyApp
import pytest

@pytest.fixture(scope='function')
def app():
    yield MyApp()

def test_app_creation(app):
    app.run_test()
