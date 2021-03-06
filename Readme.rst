Json Justify    
============                    


.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - coverage
      - | |coverage|
    * - tests
      - | |travis|  |requires|
    * - package
      - | |version|  |wheel| |supported-versions| 

.. |docs| image:: https://readthedocs.org/projects/json-justify/badge/?version=latest
    :target: https://json-justify.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |coverage| image:: https://coveralls.io/repos/github/AngrySoilder/json-justify/badge.svg?branch=master
    :target: https://coveralls.io/github/AngrySoilder/json-justify?branch=master

.. |travis| image:: https://travis-ci.org/AngrySoilder/json-justify.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/AngrySoilder/json-justify

.. |requires| image:: https://requires.io/github/AngrySoilder/json-justify/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/AngrySoilder/json-justify/requirements/?branch=master

.. |version| image:: https://img.shields.io/badge/pypi-0.1-blue.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/justify/

.. |wheel| image:: https://img.shields.io/badge/wheel-true-blue.svg
    :alt: PyPI Wheel
    :target:  https://pypi.org/project/justify/

.. |supported-versions| image:: https://img.shields.io/badge/python-3.5|3.6-blue.svg
    :alt: Supported versions
    :target: https://pypi.org/project/justify/

.. end-badges


Installation
============
This project only supports python3 version python2 support may come in upcomming versions

via pip
-------
.. code-block:: bash

    # if under linux machiene
    pip3 install justify

    # if under windows
    pip install justify

via github
----------

.. code-block:: bash

    #cloning git repo
    git clone git@github.com:AngrySoilder/json-justify.git
    cd json-justify
    python3 setup.py install 

Basic Usage
============
The basic usage of json_justify is shown here which is used to validate data from source

.. code-block:: python
    
    from json_justify import JsonManager
    from json_justify.fields import String,Number,Boolean,Array

    class Js(JsonManager):
        name = String("name")
        age = Number("age")
        male = Boolean("male")
        friends = Array("friends")

    data = {
        "name" : "john doe",
        "age" : 120,
        "male" : False,
        "friends" : ["Jelly","Kelly"]
        }
    # This will return True
    js = Js(data = data)
    data.is_valid()


Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.


Report Bugs
===========

Report bugs at https://github.com/AngrySoilder/json-justify/issues

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* If you can, provide detailed steps to reproduce the bug.
* If you don't have steps to reproduce the bug, just note your observations in
  as much detail as you can. Questions to start a discussion about the issue
  are welcome.

Submit Feedback
===============

The best way to send feedback is to file an issue at
https://github.com/AngrySoilder/json-justify/issues

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)