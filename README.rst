=====================================
Python Pypi Analysis
=====================================

This project has been created in conjunction with
`Python Pypi Fetch Top Projects https://github.com/petermcd/Python-Pypi-Fetch-Top-Projects`_

*************************************
Configuration
*************************************

This application can be configured in eiter 2 ways:

.env File
=====================================

The following is an example .env file. All entries are required apart
from port which defaults to 3306. The file must reside in the working
directory for the application.

.. code-block:: shell

   ANALYSIS_DATABASE_HOST=host
   ANALYSIS_DATABASE_NAME=name
   ANALYSIS_DATABASE_USERNAME=username
   ANALYSIS_DATABASE_PASSWORD=password
   ANALYSIS_DATABASE_PORT=3306

Environment Variables
=====================================

The configuration items that can be configured in the .env file can
also be set as environment variables.

*************************************
Development
*************************************

Git Pre Commit
=====================================

Git pre commit runs tests prior to a commit occurring, this helps
reduce CICD failures. To set this up the following commands can be
carried out:

.. code-block:: shell

   pip install pre-commit
   pre-commit install
