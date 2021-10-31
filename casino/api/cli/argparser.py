import argparse

def get_cmdl_args(args: list, description: str) -> argparse.ArgumentParser:
    """Simple command line parser
    Args:
        args (list): the input arguments from command prompt
        return (list) : the list of parsed arguments
    """
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="mode")
    # the trainer arguments
    add_tr = subparsers.add_parser('tr', help="run in training mode")
    # add_tr.add_argument("--seed", type=int, default=config.random_seed, 
    #     help="the seed globally set across the experiment. If not set, will take whatever is in src/config.py")

    # the play arguments
    add_play = subparsers.add_parser('play', help="run in evaluation/simulator mode. ")
    add_play.add_argument("play_with", type=str, choices=["human, monte, td"], help="type one of: [human (play as human), monte (monte carlo agent plays), td (td learned agent plays)]")
    add_play.add_argument("game", type=int, choices=[0], help="you can play these games: [0=easy21, ... no others yet]")
    args = parser.parse_args(args)

    return args