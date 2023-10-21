from typing import Dict


def __init():
    import pathlib
    from dotenv import dotenv_values

    return dotenv_values(pathlib.Path(__name__).parent.parent.joinpath(".env").resolve())


# Called only once
env: Dict = __init()
