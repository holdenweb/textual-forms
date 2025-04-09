## textual_forms

This is the very beginning of a forms package for textual,
(very) loosely based on the Django forms framework,
although currently with far fewer refinements
and lots of omissions.
The intention is to provide a declarative framework
for data entry and editing.

If this project is left to me it will die,
because I already know I have
neither the time
nor the energy
to support such an
effort alone.
Some interest has, however, already been expressed
by various community members
and so my hope is
that it will inspire the textual community
to help with discussions on Discord, suggestions, issues
and most valuable of all, pull requests.


As of this initial release, the _form.py_ demo shows
the (vestigial) framework's current capabilities.
Even the bits that don't actually work are credible :).

### Architecture

Note that not all aspects of the architecture are yet implemented,
and there is rather more to do than described here
to turn this into something that people will want to make use of.
Hence the need for help.

The Form class is the basis of forms development;
Forms contain one or more Fields,
each of which is associated with a Widget instance,
which may be of the Field's default type
or passed as an argument to the Field instance.

The programmer creates a Form subclass,
and within the subclass body binds a number of Field instances
to class variables.
When the form is rendered,
each of the fields' widgets in turn is rendered,
followed by one or more buttons in a row
(usually Cancel and Submit).

When the form is submitted
a FormSubmitted event is raised,
with the validated form data
available as an attribute of the event.
If the form is cancelled
a FormCancelled event is raised.

### Specific refactorings

This package is currently vestigial, with the barest proof-of-concept
demonstrating a fragile ability to turn Form subclasses into
displayable textual objects.
The existing "framework" needs to be elaborated to improve and
formalise the Form-Field and the Field-Widget interfaces.
Many of the concept from the Django forms package will prove
to be of assistance here, since it has solved many of the
domain's problems.
