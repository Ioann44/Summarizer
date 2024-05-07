from datetime import datetime, timezone
from typing import Dict, List, Tuple

from . import entities
from ..common.global_utils import Session


def get_all() -> List[entities.Text]:
    with Session() as session:
        return session.query(entities.Text).all()


def get_one(hash: str) -> entities.Text | None:
    with Session() as session:
        text = session.query(entities.Text).filter_by(hash=hash).first()
        return text


def get_with_date_update(hash: str):
    return update({"hash": hash, "lastModDate": str(datetime.now(timezone.utc))})


def add(text_dct: Dict) -> entities.Text:
    text = entities.Text(**text_dct)
    with Session() as session:
        session.add(text)
        session.commit()
        return get_one(str(text.hash))  # type: ignore


def update(dct_upd: Dict):
    with Session() as session:
        session.query(entities.Text).filter_by(hash=dct_upd["hash"]).update(dct_upd)
        session.commit()
        return get_one(dct_upd["hash"])


def delete(hash: str):
    with Session() as session:
        text = get_one(hash)
        if text is not None:
            session.delete(text)
            session.commit()
            return True
        return False


# add deletion of all expired


# # delete all
# with Session() as session:
#     session.query(entities.Text).delete()
#     session.commit()
