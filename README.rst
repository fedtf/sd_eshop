#################################################
Simple products REST api
#################################################


Running
================

To run server in docker

.. code-block:: sh

    make run_in_docker

For the rest you'll need to run mongo yourself, e.g.:

.. code-block:: sh

    docker run -d -p 27017:27017 mongo

If your mongo requires authenication set ``MONGO_USER`` and ``MONGO_PASS`` environment variables.

Setup virtualenv

.. code-block:: sh

    make setup_virtualenv

install requirements

.. code-block:: sh

    make install_requirements

run local dev server

.. code-block:: sh

    make run

or do all this with single command

.. code-block:: sh

    make run_from_scratch

To run tests

.. code-block:: sh

    make test

Example requests
================

Add product:

.. code-block:: sh

    curl -H "Content-Type: application/json" \ 
    -d '{"name":"item","description":"item description", "properties": {"weight": "30"}}' \ 
    http://localhost:8080/products/

List all products:

.. code-block:: sh

    curl http://localhost:8080/products/

Filter product list by name:

.. code-block:: sh

    curl 'http://localhost:8080/products/?name=item'


Filter product list by property value:

.. code-block:: sh

    curl 'http://localhost:8080/products/?property=weight&value=30'


Filter product list by existence of property:

.. code-block:: sh

    curl 'http://localhost:8080/products/?property=weight'


Fetch product details by id:

.. code-block:: sh

    curl http://localhost:8080/products/{id}/
