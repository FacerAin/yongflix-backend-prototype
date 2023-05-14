import io
import os
from datetime import datetime

from fastapi import APIRouter, UploadFile
from minio import Minio

from database.connection import Database
from models.videos import Video

router = APIRouter(tags=["Video"])
Database = Database(Video)


def upload_file(data):
    print(os.getenv("MINIO_ACCESS_KEY"))
    client = Minio(
        "localhost:9000/",
        access_key="oFaJsqWTypO0JVmP",
        secret_key="Zi4LfJ7PBqituyiXPLGfOEnmpMRbyRMx",
        secure=False,
    )

    bucket_name = "videos"
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    else:
        print(f"Bucket {bucket_name} already exists")
    date_time = datetime.now()

    file_path = f"video-" + str(date_time) + ".mp4"
    with io.BytesIO(data) as bin_data_io:
        client.put_object(
            bucket_name,
            file_path,
            bin_data_io,
            length=len(data),
            content_type="video/mp4",
        )

    return {"bucket_name": bucket_name, "file_path": file_path}


@router.post("/upload")
async def upload_video(video_file: UploadFile):
    upload_file(video_file.file.read())
    return {"file_name": video_file.filename}
