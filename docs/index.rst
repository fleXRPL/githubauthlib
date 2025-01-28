# docs/index.rst
.. githubauthlib documentation master file

Welcome to githubauthlib's documentation!
=======================================

GitHub Authentication Library
---------------------------

A Python library for securely retrieving GitHub tokens from system keychains across different operating systems.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   contributing

Installation
-----------

You can install githubauthlib using pip:

.. code-block:: bash

   pip install githubauthlib

Basic Usage
----------

Here's a simple example of how to use githubauthlib:

.. code-block:: python

   from githubauthlib import get_github_token, GitHubAuthError

   try:
       token = get_github_token()
       if token:
           print("Token retrieved successfully!")
   except GitHubAuthError as e:
       print(f"Error retrieving token: {e}")

API Reference
------------

.. automodule:: githubauthlib.github_auth
   :members:
   :undoc-members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
