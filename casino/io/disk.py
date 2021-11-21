import json
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def write_json(path: str, data):
    """Save data to json

    Args:
        path (str): filepath
        data (object): the jsonlike data

    Returns:
        bool: true if the save was a success
    """
    with open(path, 'w') as f:
        json.dump(data, f)
    logger.info(f"Saved json file @ path {path}.")

def read_json(path: str):
    """Save data to json

    Args:
        path (str): filepath
        data (object): the jsonlike data

    Returns:
        bool: true if the save was a success
    """
    with open(path, 'w') as f:
        data = json.load(f)
    logger.info(f"Read json file @ path {path}.")
    return data

def write_dict_as_json(path: str, data: dict, key_type: type, val_type: type):
    """Save a dict with tuple keys to json

    Args:
        path (str): filepath
        data (object): the jsonlike data
        key_type (type): the type to cast the key to
        val_type (type): the type to case the value to

    Returns:
        bool: true if the save was a success
    """
    with open(path, 'w') as f:
        json.dump({key_type(k): val_type(v) for k,v in data.items()}, f)
    logger.info(f"Saved json file @ path {path}.")

def read_q_as_dict(path: str) -> dict:
    """Read json in as a dict, expecting tuple keys with list values.

    Args:
        path (str): filepath
        data (object): the jsonlike data
        key_type (type): the type to cast the key to
        val_type (type): the type to case the value to

    Returns:
        dict: the q value read in.
    """
    logger.info(f"Attempting to read in file @ {path}")
    with open(path, 'r') as f:
        data = json.load(f)
    logger.info(f"Read json file to dict @ path {path}.")
    return {eval(k): np.array(v) for k,v in data.items()}

def write_numpy_as_csv(path: str, data: np.array, header: list):
    pd.DataFrame(data).to_csv(path, header=header)