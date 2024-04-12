import io
import pickle
from typing import Any

from ..common.global_utils import mclient


def put_text(data: str, file_name: str):
    data_encoded = data.encode()
    mclient.put_object("files", file_name, io.BytesIO(data_encoded), len(data_encoded))


def get_text(file_name: str) -> str:
    return mclient.get_object("files", file_name).read().decode()


def save_pickle(obj: Any, file_name: str):
    bytes = pickle.dumps(obj)
    mclient.put_object("files", file_name, io.BytesIO(bytes), len(bytes))


def load_pickle(file_name: str):
    return pickle.loads(mclient.get_object("files", file_name).read())
