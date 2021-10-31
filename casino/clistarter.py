from casino.logging import logutil
from casino.util import io
from casino.api.cli import argparser
from casino.agents.gamerunner import GameRunner
import logging

logger = logging.getLogger(__name__)

def setup(base_dir):
    log_dir = "logs"
    session_start = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    io.inititialize_dirs([log_dir])
    logutil.setup_global_file_logging('%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                      "%y-%m-%d %H:%M:%S",
                                      os.path.join(base_dir, log_dir, f"session{session_start}"))

    logger.info(f"Starting up casino @{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

    return session_start

def run(base_dir, session_start):
    """Run method for casino with CLI. 


    Args:
        base_dir (str): the base directory for casino
        session_start (str) : the str timestamp for startup
    """
    args = argparser.get_cmdl_args(sys.argv)

    if args.mode == "tr":
        pass
    if args.mode == "play":
        GameRunner(args.game, args.play_with).run()


if __name__=="__main__":
    start_time = setup(sys.path[0])
    run(sys.path[0], start_time)