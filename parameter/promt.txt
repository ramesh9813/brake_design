Task: Build a Flask-based web application for motorcycle disc brake design.

Environment setup

Create a virtual environment named design_env.

Install all required Python modules (flask, numpy, scipy, etc.).

Inputs (user-provided via web form)

The user will enter:

Mass of vehicle (kg)

Mass of rider and load (kg)

Desired deceleration / stopping distance (m or m/s²)

Material properties (density, yield strength, modulus, specific heat, etc.)

Outputs (computed after form submission)

Outer diameter of disc brake

Inner diameter of disc brake

Thickness of disc brake

Maximum stress generated

Functional requirements

The landing page (/) should display a simple toolbox list.

One of the tools should be “Disc Brake Design”.

When user clicks Disc Brake Design, they are taken to a form page (/disc-brake) with input fields for the required variables.

On form submission:

Flask reads the inputs.

A backend calculation function computes the brake disc dimensions & stress.

Results are displayed in the UI, styled in Courier font.

UI / Website design

Use Flask routes only (no extra frontend frameworks required).

Consistent header and footer across all routes.

Header/footer should be minimal and attractive.

Form should look clean and simple.

Results section should clearly display calculated values in Courier font.

Tools & libraries

Python

Flask

NumPy / SciPy (for calculations)

HTML + CSS (Jinja templates for pages)