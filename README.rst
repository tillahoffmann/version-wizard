🧙 version-wizard
=================

.. image:: https://github.com/tillahoffmann/wizard-version/actions/workflows/main.yml/badge.svg
    :target: https://github.com/tillahoffmann/wizard-version/actions/workflows/main.yml
.. image:: https://badge.fury.io/py/version-wizard.svg
    :target: https://pypi.org/project/version-wizard/

The version wizard extracts version information from a git tag and includes it in your python package so you don't have to worry about commit messages like :code:`Bump version to 0.8.1` anymore. Here's how to use the wizard:

1. Install by running :code:`pip install version-wizard`.
2. Add :code:`include VERSION` to your :code:`MANIFEST.in` file (or create one by running :code:`echo "include VERSION" > MANIFEST.in`).
3. Update your :code:`setup.py` as shown below.
4. Push `semantic versioning <https://semver.org>`_ tags to your GitHub branch, e.g, :code:`0.8.1`.

.. code-block:: python

    # setup.py
    from setuptools import setup, ...
    from version_wizard import from_github_tag

    setup(
        version=from_github_tag(),
        ...
    )

Behind the scenes
-----------------

The call to :code:`from_github_tag` will do one of two things:

1. If the :code:`VERSION` file exists, it simply returns its contents. This is the typical behavior when your installing the package from pypi, for example.
2. If the :code:`VERSION` file does *not* exist, it will try to extract the version from the :code:`GITHUB_REF` environment variable and write it to the :code:`VERSION` file.

Because the :code:`MANIFEST.in` includes :code:`VERSION`, the :code:`VERSION` file will be included in any distribution, e.g., when you run :code:`python setup.py sdist`. The correct version is thus automatically packaged with your distribution elminiating any possible inconsistencies.

Interface
---------

.. automodule:: version_wizard
    :members:
