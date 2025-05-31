## Fields and Widgets

The value of a field is set using Python values, so for example the IntegerField should be set with int values, and will return int values.
When a field value is set, it in turn sets the value of a widget using whatever type the widget expects.
So, to follow the same example, the IntegerWidget subclasses `Input`
and when the IntegerField is set the Field must convert the int to a string before assigning it to the widget field.
Conversely, when you read a field's value it reads the widget's value and performs any necessary conversion to the expected Python type.