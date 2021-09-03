# Python packaging

Useful links:

- The giude: https://packaging.python.org/tutorials/packaging-projects/
- Also something, not used here much: https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html


## Pushing new update

1. Update the code and commit
2. Update the version in `setup.cfg` and commit
3. Build the project by `python -m build`
4. Upload the built files in `dist/*` to PyPi by `python -m twine upload dist/*`
    1. Username: `__token__`
    2. Password: the token from pypi
5. Done, now the package can be downloaded by people


## Downloading the package in a venv

1. Create an empty folder and enter it
2. Run `python -m venv .` to create virtual environment
    1. The venv will not contain mashcima even if I have it installed globally
3. Install mashcima by `bin/pip install mashcima`
    1. Pin the development version `bin/pip install mashcima==0.0.2.dev0`
4. Start the python interpreter and play with it `bin/python`
