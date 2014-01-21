.. aws-tools documentation master file, created by
   sphinx-quickstart on Wed Jan 15 02:04:21 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aws-tools's documentation!
=====================================

My AWS Tools

:github: https://github.com/toomore/aws-tools
:requirement: `boto <https://github.com/boto/boto>`_

.. toctree::
   :numbered:

   AwsEC2Tools <awsec2tools>
   AwsSESTools <awssestools>
   AwsS3Tools <awss3tools>
   AwsSQSTools <awssqstools>
   Some scripts <scripttools>

What Tools
============

AwsEC2Tools
---------------

1. Auto snapshot. (create_snapshot)
2. Created from AMIs in VPC. (register_image, run_from_image)
3. Created spot instances in VPC. (run_spot_instances_from_image, get_spot_price_history)

.. seealso:: :doc:`./awsec2tools`

AwsEC2MetaData
---------------

1. Get EC2 meta-data info.

.. seealso:: :doc:`./awsec2tools`

AwsSESTools
---------------

1. Sender with UTF-8 charset.

.. seealso:: :doc:`./awssestools`

AwsS3Tools
---------------

1. CRUD files by using S3.
2. #TODO update key with the same acl.

.. seealso:: :doc:`./awss3tools`

AwsSQSTools
---------------

1. write/get messages.
2. #TODO increase ``get_messages`` concurrency.

.. seealso:: :doc:`./awssqstools`

Target
========

1. SQS Worker.
2. SES with html template.
3. gevent.

Some scripts
=============

.. seealso:: :doc:`./scripttools`

TODO List
===========

.. todolist::


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

