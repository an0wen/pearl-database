.. PEARL Backend documentation master file, created by
   sphinx-quickstart on Sun Jul 26 20:06:51 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PEARL Backend documentation
===========================

PEARL — the Planetary EOS Archive and Reference Library — is an open
catalog of thermodynamic data and equations of state.

This documentation describes the Python backend used to load, validate,
search, manipulate, plot, and export the database contents.

.. note::

   PEARL is under active development. Interfaces and data conventions may
   change before the first stable release.

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   getting_started/installation
   getting_started/repository_structure
   getting_started/dependencies   

.. toctree::
   :maxdepth: 2
   :caption: Data format

   data_format/reference

.. User Guide pages will be added later.
   .. toctree::
      :maxdepth: 2
      :caption: User guide

      .. user_guide/database_structure
      .. user_guide/loading
      .. user_guide/searching
      .. user_guide/plotting
      .. user_guide/exporting

   .. toctree::
      :maxdepth: 2
      :caption: Contributor guide

      .. contributor_guide/data_conventions
      .. contributor_guide/adding_data
      .. contributor_guide/adding_eos
      .. contributor_guide/validation

   .. toctree::
      :maxdepth: 2
      :caption: Developer guide

      .. developer_guide/architecture
      .. developer_guide/testing
      .. developer_guide/design_decisions

.. toctree::
   :maxdepth: 2
   :caption: API reference

   api/index