from pydantic import BaseModel
from typing import List,Union
from fastapi import File,Form,UploadFile

class TaskRequest(BaseModel):
    query:str
    thread_id:str = None


class UpLoadContent(BaseModel):
    files:List[UploadFile]=File(...)
    thread_id:str=Form(...)
