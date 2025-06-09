# Welcome to textual-forms

The package that aims to make data collection and editing through terminals as easy as possible.

## Usage Pattern

1. Declare a form by Subclassing `textual_forms.Form`.
2. Add class variables whose values are `textual_forms.Field` specifications.
3. Mount the widget returned by the form's `render` method.
4. Handle `Form.Submitted` and `Form.Cancelled` messages.
4. Result: happiness - and data!

## A Simple Example



## Project layout

    Makefile            # Simple developer help
    mkdocs.yml          # The documentation configuration file.
    dist                # Distribution artefacts
    docs/
        index.md        # The documentation homepage.
        ...             # Other markdown pages, images and other files.
    images/             # Pictures for README and docs
    src/                # Source code for developer tools &c.
        textual_forms/  # Source code for the package
    tests               # Yes, we have tests

