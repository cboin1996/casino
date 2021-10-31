import logging

def setup_global_logging_stream(fmt: str):
    """Setup the logging for the package.

    Args:
        fmt (str): how to format the logging
    """
    console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def setup_global_file_logging(fmt: str, date_fmt: str, fpath: str):
    """Setup logging to files globally

    Args:
        fmt (str): the format for the logging
        date_fmt (str): the date format for the logging
        fpath (str): full path for log file
    """
    logging.basicConfig(level=logging.INFO,
                    format=fmt,
                    datefmt=date_fmt,
                    filename=fpath,
                    filemode='w')