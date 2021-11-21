import argparse

def get_cmdl_args(args: list, description: str) -> argparse.ArgumentParser:
    """Simple command line parser
    Args:
        args (list): the input arguments from command prompt
        return (list) : the list of parsed arguments
    """
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="mode", help="Which mode to run in.")

    # the play arguments
    add_play = subparsers.add_parser("play", help="run in play mode. ")
    add_play.add_argument("--agent", type=str, default="human", choices=["human", "monte", "td"], help="type one of: [human (play as human), monte (monte carlo agent plays), td (td learned agent plays)]")
    add_play.add_argument("--game", type=int, default="game", choices=[0], help="you can play these games: [0=easy21, ... no others yet]")
    add_play.add_argument("--debug_mode", type=int, choices=[0,1], default=0, help="dictates the logging level. Set to 0 to include all debugging level msgs.")
    # the trainer arguments
    add_tr = subparsers.add_parser("tr", help="run in trainer mode. ")
    add_tr.add_argument("--game_id", type=int, default=0, choices=[0], help="you can play these games: [0=easy21, ... no others yet]")
    add_tr.add_argument("--debug_mode", type=int, choices=[0,1], default=0, help="dictates the logging level. Set to 0 to include all debugging level msgs.")

    add_tr.add_argument("--n_episodes", type=int, default=10000, help="The number of episodes to use during training")
    add_tr.add_argument("--gamma", type=float, default=1.0, help="The discount coefficient")
    add_tr.add_argument("--policy", type=int, choices=[0], default=0, help="valid polices are: [0=epsilon greedy .. no others yet]")
    add_tr.add_argument("--eps_const", type=int, default=100, help="a constant for the epsilon exploration strategy")
    # add the agents for the trainer with their specific hyperparams
    tr_subparser = add_tr.add_subparsers(dest="agent", help="which agent to train with.")

    # monte carlo control
    add_monte = tr_subparser.add_parser("monte", help="use monte carlo control as the agent")

    add_sarsa = tr_subparser.add_parser("sarsa", help="use sarsa as the agent")
    add_sarsa.add_argument("--opt_q_path", type=str, default="", help="pass a trained q value to compare performance to using MSE.")

    add_qlearn = tr_subparser.add_parser("qlearn", help="use q_learning as the agent")
    add_qlearn.add_argument("--opt_q_path", type=str, default="", help="pass a trained q value to compare performance to using MSE.")
    args = parser.parse_args(args)

    return args