import io

from ..common.global_utils import mclient


def put_text(data: str, file_name: str):
    data_encoded = data.encode()
    mclient.put_object("files", file_name, io.BytesIO(data_encoded), len(data_encoded))
