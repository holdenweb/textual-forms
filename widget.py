from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Vertical

from field import TextField, IntegerField, BooleanField, ChoiceField
from form import Form

class MyForm(Form):
    name = TextField(label="Name", required=True)
    age = IntegerField(label="Age", required=False)
    is_active = BooleanField(label="Active")
    choice = ChoiceField(choices = [("option1","Option 1"),("option2","Option 2")], label = "Choice")

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Vertical(MyForm(), Button("Submit"), id="form_container")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        form = self.query_one(MyForm)
        if form.validate():
            data = form.get_data()
            self.notify(f"Form data: {data}")
        else:
            self.notify("Form validation failed.")

if __name__ == "__main__":
    app = MyApp()
    app.run()