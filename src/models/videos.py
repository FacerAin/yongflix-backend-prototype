from typing import List

from pydantic import BaseModel


class Video(BaseModel):
    name: str
    description: str
    like_user_id: List[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "test_video",
                "desciption": "This is a test video for testing.",
                "like_user_id": ["111", "222", "333"],
            }
        }
