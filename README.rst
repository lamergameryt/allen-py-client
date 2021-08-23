=============
AllenPyClient
=============

AllenPyClient is an unofficial Python wrapper to develop applications integrating Allen's official web API.

|Code Quality| |PyPi| |Docs| |License| |Followers|

.. |License| image:: https://img.shields.io/github/license/lamergameryt/allen-py-client
.. |Followers| image:: https://img.shields.io/github/followers/lamergameryt?style=social
.. |PyPi| image:: https://badge.fury.io/py/allen-py-client.svg
    :target: https://badge.fury.io/py/allen-py-client
.. |Docs| image:: https://readthedocs.org/projects/allenpyclient/badge/?version=latest
    :target: https://allenpyclient.readthedocs.io/en/latest/?badge=latest
.. |Code Quality| image:: https://img.shields.io/lgtm/grade/python/github/lamergameryt/AllenVideoDownloader
    :target: https://lgtm.com/projects/g/lamergameryt/AllenVideoDownloader/context:python

⏩ Quick Example
----------------

In this example, we will fetch the links of the videos available to us.

``main.py``

.. code-block:: python

    from allen import AllenClient
    import os

    env = os.environ
    user = env['user']
    passwd = env['passwd']

    client = AllenClient(username=user, password=passwd)
    videos = client.get_recorded_videos()
    for video in videos:
        link = video.get_link()

        # Print the video link with the subject name and recording date
        print(f'{video.subject_name} ({video.get_recording_date()}) - {link}')

You can also use the library from a command line.

::

    $ allen help
    $ allen videos

👩‍🏫 Installation
------------------

::

    pip install allen-py-client

📈 Required Python Modules
--------------------------

The list of required python modules can be found in the ``requirements.txt`` file.

📜 Documentation
----------------

To view the documentation for this project, visit the `documentation page <https://allenpyclient.readthedocs.io/en/latest/>`_.
