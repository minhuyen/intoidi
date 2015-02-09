__author__ = 'dominhuyen'


def make_choices(choices):
    """
    Zips a list with itself for field choices.
    """
    return list(zip(choices, choices))
