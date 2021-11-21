from typing import Set
import logging

logger = logging.getLogger(__name__)
def get_input(prompt: str, choices: set, quit_str: str, dtype: type):
    """Simple input getter

    Args:
        prompt (str): the prompt to display for the input
        choices (set): the list of choices that are valid for return
        quit_str (str): a str or character that allows the prompt look to break
        typ (type): the type to cast the input to

    Returns:
        str, None: the input, or None if quit is selected
    """
    x = None
    try_count = 0
    quit_prompt = f" [{quit_str}] exits prompt: "
    formatted_prompt = prompt + quit_prompt
    while x != quit_str:
        if try_count >= 1:
            formatted_prompt = f"Try again. Expecting on of {choices}. " + prompt + quit_prompt
        x = input(formatted_prompt)
        try:
            x = dtype(x)
            if dtype(x) in choices:
                return dtype(x)
        except ValueError:
            logger.error(f"Invalid conversion for '{x}' using dtype {dtype.__name__}")

        try_count += 1

