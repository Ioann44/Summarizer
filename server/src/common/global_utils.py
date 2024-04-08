import json


def __init():
    from typing import Dict
    import pathlib
    from dotenv import dotenv_values
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from minio import Minio
    from .base_class import Base

    env = dotenv_values(pathlib.Path(__name__).parent.parent.joinpath(".env").resolve())
    db_url = f"postgresql://user:{env['DATABASE_PASSWORD']}@{env['DATABASE_HOST']}:5432/database"
    assert db_url is not None, "DATABASE_URL is not defined"

    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    mclient = Minio(
        (env["MINIO_HOST"] or "localhost") + ":9000",
        access_key="user",
        secret_key=env["MINIO_PASSWORD"],
        secure=False,
    )
    if not mclient.bucket_exists("files"):
        mclient.make_bucket("files")
        mclient.set_bucket_policy(
            "files",
            json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": ["s3:GetObject"],
                            "Resource": ["arn:aws:s3:::files/*"],
                        }
                    ],
                }
            ),
        )

    return sessionmaker(bind=engine), mclient, env


# Called only once
Session, mclient, env = __init()
