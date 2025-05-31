# Welcome to textual-forms

The package that wants to make data collection and editing through the terminal as easy as possible.

## Basic Usage

Declare a form by Subclassing `textual_forms.Form`.
Add class variables whose values are field specifications.
Render the form and mount the resulting widget.
Result: happiness.

## Project layout


    mkdocs.yml    # The configuration file.
    dist          # Distribution artefacts
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
    images/       # Pictures for README and docs
    src/          # Source code
        textual_forms  # Source for the package
    tests         # Yes, we have tests

