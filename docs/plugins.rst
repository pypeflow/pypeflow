Plugins
=======

Excerpts
--------

Generates excerpts from file contents

Requirements
^^^^^^^^^^^^

- beautifulsoup4

Usage
^^^^^

.. code-block:: python

    from pipeflow import Pypeflow
    ...
    from pipeflow.contrib.excerpts.ExcerptsPlugin

    pypeflow = Pypeflow(
        ...
        plugins=(
            ...
            ExcerptsPlugin(size=160),
            ...
        )
    )