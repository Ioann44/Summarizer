from typing import Dict

from . import entities
from ..common.global_utils import Session


def add(poll_dct: Dict) -> entities.PollRes:
    poll = entities.PollRes(**poll_dct)
    with Session() as session:
        session.add(poll)
        session.commit()
        session.refresh(poll)
        return poll
