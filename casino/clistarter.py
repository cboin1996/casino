import argparse
from casino.logutil import logutil
from casino.util import io
from casino.api.cli import argparser
from casino.workers.gamerunner import GamePlayer
from casino.util.env import varia

import logging

import os, datetime, sys

logger = logging.getLogger(__name__)

def setup(base_dir, args: argparse.ArgumentParser):
    session_start = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    io.inititialize_dirs([varia.LOG_DIR, varia.DATA_DIR])
    logutil.setup_global_file_logging('%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                      "%y-%m-%d %H:%M:%S",
                                      os.path.join(base_dir, varia.LOG_DIR, f"session{session_start}"),
                                      bool(args.debug_mode))

    logutil.setup_global_logging_stream('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', bool(args.debug_mode))
    logger.info(f"Starting up casino @{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return session_start

def run(base_dir, args: argparse.ArgumentParser, session_start: str):
    """Run method for casino with CLI. 


    Args:
        base_dir (str): the base directory for casino
        session_start (str) : the str timestamp for startup
    """

    if args.mode == "tr":
        game = GamePlayer(base_dir, session_start, args)
        game.setup()
        game.train_session()
    if args.mode == "play":
        game = GamePlayer(base_dir, session_start, args)
        game.setup()
        game.play()
    if args.mode == "eval":
        game = GamePlayer(base_dir, session_start, args)
        game.evaluate()

if __name__=="__main__":
    logger.info("Launching CLI!")
    args = argparser.get_cmdl_args(sys.argv[1:], 'Welcome to Casino \|\!')
    
    start_time = setup(sys.path[0], args)
    run(sys.path[0], args, start_time)