from typing import List

import os, sys
import logging

logger = logging.getLogger(__name__)

def inititialize_dirs(dirs: List[str]):
    """create directories if they do not exist

    Args:
        dirs (List[str]): the list of directories to create
    """
    for directory in dirs:
        dir_path = os.path.join(sys.path[0], directory)
        if not os.path.exists(dir_path):
            logger.info(f"Making dir {dir_path}")
            os.mkdir(dir_path)