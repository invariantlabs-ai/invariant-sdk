# Invariantlabs Client SDK

This repository contains the Python SDK for interacting with the [Invariantlabs](https://invariantlabs.ai/) APIs.

## Run tests
1. To run tests run `pytest`.
2. To run tests with coverage run `pytest --cov=invariant`.
3. To run tests with coverage (to also include a HTML report) run `pytest --cov=invariant --cov-report=html`. You can then open the `index.html` file in the `htmlcov` folder in your browser to see more coverage details by functions or classes.

For additional details add the `-s` and `-vv` flags when running pytest:
- `-s`: Allowing you to see print statements and other standard output.
- `-vv`: Increase verbosity, providing more detailed information about each test.