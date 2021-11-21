import logging
import sys

def setup_global_logging_stream(fmt: str, debug_mode: bool):
    """Setup the logging for the package.

    Args:
        fmt (str): how to format the logging
    """
    console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt)
    console.setFormatter(formatter)
    if not debug_mode: # default use info as logging to stream
        console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

def setup_global_file_logging(fmt: str, date_fmt: str, fpath: str, debug_mode):
    """Setup logging to files globally

    Args:
        fmt (str): the format for the logging
        date_fmt (str): the date format for the logging
        fpath (str): full path for log file
    """
    if (debug_mode):
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level,
                    format=fmt,
                    datefmt=date_fmt,
                    filename=fpath,
                    filemode='w')