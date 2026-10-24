import asyncio
import shutil

from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile,WebSocket,WebSocketDisconnect
from typing import Annotated,Any,List
from app.mainagent.primary_agent import run_deep_agent
from app.db_orm.load_and_transform_data.load_and_transform import update_data_to_mysql
from fastapi.responses import FileResponse
from uuid import uuid4
from pathlib import Path
from api.schema.schema import TaskRequest,UpLoadContent
from base_config.logger.logger import logger



api_router = APIRouter(prefix="/api")

active_tasks:dict[str,asyncio.Task] = {}

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

output_dir = project_root / "save_dir" / "output"
output_dir.mkdir(parents=True,exist_ok=True)

updated_dir = project_root/ "save_dir" / "updated"
updated_dir.mkdir(parents=True,exist_ok=True)



def _delete_task(thread_id:str,task:asyncio.Task):
    if active_tasks.get(thread_id) is task:
        active_tasks.pop(thread_id,None)


@api_router.post("/start")
async def run_task(request:TaskRequest):
        thread_id = request.thread_id or str(uuid4())[:10]
        old_task = active_tasks.get(thread_id)
        if old_task and not old_task.done():
            old_task.cancel()

        task = asyncio.create_task(run_deep_agent(request.query,thread_id))
        active_tasks[thread_id] = task
        task.add_done_callback(lambda x_task:_delete_task(thread_id,x_task))
        return {"status":"start","thread_id":thread_id}


@api_router.post("/cancel")
async def cancel_task(thread_id:str):
    task = active_tasks.get(thread_id,"")
    if task:
        if hasattr(task,"done"):
            if task.done():
                await active_tasks.pop(thread_id,None)
                raise HTTPException(status_code=211, detail="任务不存在或已经结束")
    else:
        raise HTTPException(status_code=211,detail="Task not exists or is over")

    task.cancel()
    try:
        await asyncio.wait_for(task,timeout=1.0)
    except asyncio.CancelledError:
        _delete_task(thread_id,task)
        return {"status":"cancelled","thread_id":thread_id}
    except asyncio.TimeoutError:
        return {"status":"cancelling","thread_id":thread_id}
    except Exception as e:
        _delete_task(thread_id,task)
        return {"status":"cancelled","thread_id":thread_id,"message":str(e)}

    _delete_task(thread_id,task)
    return {"status":"cancelled","thread_id":thread_id}





@api_router.post("/upload")
async def upload_files(files:List[UploadFile]=File(...),thread_id:str=Form(...)):
#async def upload_files(request:UpLoadContent):#这种使用校验的方式不可行，file和thread_id走的是multipart/form-data格式，如果使用Pydantic模型校验就要是application/json格式，因此会报UnicodeDecodeError
    target_dir = updated_dir / f"session_{thread_id}"
    target_dir.mkdir(parents=True,exist_ok=True)

    saved_files = []
    for file in files:
        file_path = target_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        saved_files.append(file.filename)

    return {"status":"uploaded","files":saved_files}



@api_router.get("/download")
async def download_file(path:str):
    logger.info(path)
    try:
        abs_path = Path(path).resolve()
        output_abs = output_dir.resolve()

        if not abs_path.is_relative_to(output_abs):
            return {"error":"拒绝访问：只能下载输出目录下的文件"}
    except Exception as e:
        return {"error":f"无效路径 -- {str(e)}"}

    if not abs_path.exists():
        return {"error":"文件不存在"}

    return FileResponse(abs_path,filename=abs_path.name)


@api_router.get("/files")
async def list_files(path:str):
    print(f"[DEBUG]请求文件列表:{path}")

    abs_path = Path(path).resolve()
    output_abs = output_dir.resolve()

    try:
        if not abs_path.is_relative_to(output_abs):
            print(f"[ERROR] 拒绝访问:{abs_path}不在{output_abs}目录下")
            return {"error":"拒绝访问：只能访问输出目录下的文件"}
    except Exception as e:
        print(f"[ERROR] 路径解析失败:{e}")
        return {f"error":"路径无效--{str(e)}"}

    if not abs_path.exists():
        return {"error":"目录不存在"}

    files = []
    try:
        for file_path in abs_path.rglob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append(
                    {
                        "name":file_path.name,
                        "type":"file",
                        "path":str(file_path),
                        "size":stat.st_size,
                        "mtime":stat.st_mtime
                    }
                )
    except Exception as e:
        print(f"[ERROR] 遍历文件失败:{e}")
        return {"error":f"{str(e)}"}

    files.sort(key=lambda x: x.get("mtime",0),reverse=True)
    print(f"[DEBUG] 找到{len(files)}个文件")
    return {"files":files}


#两种方法调用函数
#写入数据到数据库中
@api_router.get("/update")
async def updated_mysql(request:TaskRequest):

    old_task = active_tasks.get(request.thread_id)
    if old_task and not old_task.done():
        old_task.cancel()


    task = asyncio.create_task(update_data_to_mysql())
    active_tasks[request.thread_id] = task
    task.add_done_callback(lambda x_task:_delete_task(request.thread_id,x_task))
    return {"status":"update..."}


#async def updated_mysql(service:Annotated[Any,Depends(update_data_to_mysql)])
    #return service








