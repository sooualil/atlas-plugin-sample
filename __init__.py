import json
from random import randint
from time import time
from typing import Dict, List
import uuid

import numpy as np
from core.database import __db__
from core.logger import Logger
from .model import Model
from model.configuration.extension import InferenceConfig
from util.functions import loadConfig, relative, timestamp

try:
    # load and parse configuration
    config = loadConfig(InferenceConfig, relative(__file__, './config.yaml'))

    # Register extension channels into the current instance of the database manager
    __db__.register_extension(config)

    # Get logger
    logger = Logger(config.log, __name__.split('.')[-1])

    # Load ML model
    ml = Model(relative(__file__, config.data.model))

    # Counter to stop extension
    i = 0
    t = time()

    batch: Dict[str, List] = {}
    batch_indexing = []

    # Iterated over subscribed channels
    for data in __db__.get_message():
        # check if is is a message from the publisher
        if data['type'] == 'message':
            # Log received flow
            # logger.debug('Received flow', data['data'], 'and storing inference', i)
            
            i+=1
            if time() - t > 3: 
                logger.debug(f'{i} items processed')
                t = time()

            # Retrieve flow id
            flow_id = data['data']

            flow: Dict = __db__.retrieve('flow', flow_id)
            for k, v in flow.items():
                if k not in batch: batch[k] = []
                batch[k].append(v)

            batch_indexing.append(flow_id)

            if len(batch[k]) < config.data.batch_size:
                continue
            
            _, predictions = ml.predict(batch)

            batch = {}
            # Generate random prediction
            pred_data = {
                'id': uuid.uuid4().hex,
                'predictions': {batch_indexing[i]: p for i, p in enumerate(predictions)}
            }

            # Store prediction
            __db__.store('inference', pred_data['id'], pred_data)

            # Publish the id of the prediction configured channels
            for ch in config.channels.publish: __db__.publish(ch, pred_data['id'])
except KeyboardInterrupt:
    print('aight bye')
    __db__.stop_listening()
