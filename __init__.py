from core.logger import Logger
from model.configuration.extension import Configuration
from core.database import __db__

from util.functions import loadConfig, relative, timestamp
try:
    # load and parse configuration can be FeatureConfig, InferenceConfig, or ReportingConfig
    config = loadConfig(Configuration, relative(__file__, './config.yaml'))

    # Get logger
    logger = Logger(config.log, __name__.split('.')[-1])


    # for inpt in config.channels.input:
    for data in __db__.get_message():

        # Do awesome stuff ..

        # Store data in the database
        __db__.store(name, key, value)

        # Trigger publish
        for ch in config.channels.publish:
            __db__.publish(ch, results)


except KeyboardInterrupt:
    print('aight see ya')