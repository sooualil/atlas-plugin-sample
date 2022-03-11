# Atlas extension

This a simple hello world extension for Atlas IDS engine.

# Installation

This is the default extension that can be generate using Atlas tool `atlas` or from source `python app.py`

    atlas feature hello-world
    atlas inference hello-world
    atlas reporting hello-world

If it is a custom extension clone the repository in your Atlas extensions folder.

    cd path/to/atlas-ids
    cd extensions/feature
    git clone https://github.com/sooualil/atlas-plugin-sample.git

# Examples

## Feature extension

This is an example application that reads data from the input specified in the config and publishes it through [Redis](https://github.com/redis/redis) :


    python
    # TODO


The flow is saved in the database and only the ID is published to keep the message broker use the least data possible.


