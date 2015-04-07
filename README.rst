Just docs downloader
====================
A Python_ script to download all non-design docs from a CouchDB_ database.  Useful for automated backups into a simple text file.

CouchDB's ``_all_docs`` API returns all keys, or all docs, or a subset based on numeric indexes, but cannot easily filter specific documents by their ids.  Since design documents are normally very large, and usually do not need to be backed up (since they are typically code installed into CouchDB), this script filters them out and then writes the JSON to a text file.

Installation
++++++++++++
#. Install Python_.
#. Install pip_, if necessary.
#. ``pip install -r requirements.txt``

Usage
+++++
::

    # To show all options.
    just-docs-downloader.py --help

    # Example call, without authentication.
    just-docs-downloader.py --serverurl http://127.0.0.1:5984 --dbname=any-database \
    --output=/full/path/to/output.file

    # Example call, with basic authentication.
    just-docs-downloader.py --serverurl http://127.0.0.1:5984 --dbname=any-database \
    --output=/full/path/to/output.file --username=user --password=p@$$w0rd



.. _pip: https://pip.pypa.io/
.. _python: http://www.python.org/
.. _couchdb: http://couchdb.apache.org/
