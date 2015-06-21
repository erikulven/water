Water
==========

Collects and presents water levels in Norwegian rivers


Getting started:
================
 .. code-block:: shell
 
    Create virtualenv with python3.4
    $ virtualenv --python=/usr/local/bin/python3.4 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

 
    $ cd <src-root>
    $ export PYTHONPATH=`pwd`

    $ python app.py


   
Setup FreeBSD (10+):
====================

Some pip's need to be built from ports with python3.4.

.. code-block:: shell

    /usr/ports/databases/py-sqlite3# make PYTHON_VERSION="python3.4" install
    /usr/ports/security/py-pycrypto# make PYTHON_VERSION="python3.4" install

Create virtualenv, using system packages.

.. code-block:: shell

    $ cd <fw-src> 
    $ virtualenv --system-site-packages --python=/usr/local/bin/python3.4 venv
    $ source venv/bin/activate.csh
    $ pip install -r requirements.txt

SSL verification:
-----------------
Might need to install  security/ca_root_nss.

Check if python can find ssl cert. Python 3.4+, 2.7.9 uses openssl which looks
 in /etc/ssl/
Symlink can fix it if /etc/ssl/cert.pem doesn't exist.
For more info: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=196431

.. code-block:: shell

    # ln -s /usr/local/etc/ssl/cert.pem /etc/ssl/cert.pem# water
