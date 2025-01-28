# How to include your package in the Python Package Index (PyPI) and make it installable via `pip`

## Follow these general steps

1. Create a `setup.py` file:

    Create a `setup.py` file in the root directory of your package. This file contains the metadata about your package, such as its name, version, description, and other relevant information.

    Here's an example `setup.py` file:

    ```python
    """

    Setup file for githubauthlib

    """

    from setuptools import setup, find_packages

    setup(
        name="githubauthlib",
        version="1.0",
        description='A library for authenticating with GitHub',
        author='garotm',
        install_requires=[
            'subprocess',
            'platform',
        ],
        packages=find_packages(),
    )
    ```

2. Build the distribution files:
Use the `setuptools` library to create the distribution files for your package. Open a terminal or command prompt, navigate to the root directory of your package (where the `setup.py` file is located), and run the following command:

    ```bash
    python setup.py sdist bdist_wheel
    ```

    This will generate two types of distribution files: a source distribution (`sdist`) and a wheel distribution (`bdist_wheel`). These files will be used for distribution and installation.

3. Register on PyPI:
Before you can upload your package to PyPI, you need to create an account on PyPI if you don't have one already. Go to the PyPI website [pypi.org](https://pypi.org/) and sign up for an account.

4. Install twine:
You'll need `twine` to securely upload your package to PyPI. If you don't have it installed, you can install it using `pip`:

    ```bash
    pip install twine
    ``````

5. Upload the package to PyPI:
Use `twine` to upload your package to PyPI. Run the following command:

    ```bash
    twine upload dist/*
    ```

    This command will prompt you to enter your PyPI username and password or ask for your API token if your .pypirc file is configured with an API token.

    If you've configured a .pypirc file with your credentials, you can use the following command instead to bypass manual entry of credentials:

    ```bash
    twine upload --config-file ~/.pypirc dist/*
    ```

    expected output:

    ```bash
    MAC-01:githubauthlib garotm$ twine upload --config-file ~/.pypirc dist/*
    Uploading distributions to https://upload.pypi.org/legacy/
    Uploading githubauthlib-1.0-py3-none-any.whl
    100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 kB • 00:02 • ?
    Uploading githubauthlib-1.0.tar.gz
    100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.4/4.4 kB • 00:00 • ?

    View at:
    https://pypi.org/project/githubauthlib/1.0/
    
    ```

    After successful upload, your package will be available on PyPI for installation.

6. Verify Your Package on PyPI:
Go to your package's [PyPI page](https://pypi.org/project/githubauthlib/1.0/) to make sure the package and its version are correctly listed.

7. Install your package using `pip`:
Now that your package is on PyPI, you can install it using `pip` like any other package:

    ```bash
    pip install githubauthlib
    ```

    Replace `githubauthlib` with the actual name you specified in the `setup.py` file.

---

That's it! Your package is now available on PyPI and can be easily installed by others using `pip install githubauthlib`.

Keep in mind that publishing packages on PyPI is a public act, and it's essential to ensure your code is properly documented, well-tested, and adheres to best practices. Make sure to thoroughly test your package and keep it up-to-date with new releases if necessary.
