import asyncio
import builtins
import datetime
from typing import Any,Optional
from fastapi import WebSocket
from api.context.context import get_thread
from base_config.logger.logger import logger



class ToolMonitor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolMonitor,cls).__new__(cls)
            cls._instance.websocket_manager = None
        return cls._instance


    def set_websocket_manager(self,manager:"ConnectionManager")->None:
        self.websocket_manager = manager


    def _emit(
            self,
            event_type:str,
            message:str,
            data:Optional[dict[str,Any]] = None
    )->None:
        payload = {
            "type":"monitor_event",
            "event":event_type,
            "message":message,
            "data":data or {},
            "timestamp":datetime.datetime.now().isoformat()
        }


        if self.websocket_manager:
            try:
                thread_id = get_thread()
                manager_loop = self.websocket_manager.loop

                if manager_loop and thread_id:
                    self._send_to_websocket(payload,thread_id,manager_loop)
            except Exception as e:
                logger.warning(f"[Monitor] WebSocket send failed :{e}")


        if hasattr(builtins,"runtime") and hasattr(builtins.runtime,"stream_writer"):
            try:
                builtins.runtime.stream_writer(payload)
            except Exception as e:
                logger.warning(f"不存在运行时状态:{e}")

        logger.info(f"\n[Monitor]:{event_type}-{message}-{data}")


    def _send_to_websocket(
            self,
            payload:dict[str,Any],
            thread_id:str,
            manager_loop:asyncio.AbstractEventLoop
    ):
        try:
            current_loop = asyncio.get_running_loop()
        except RuntimeError:
            current_loop = None

        coroutine = self.websocket_manager.send_to_thread(payload,thread_id)


        if current_loop and current_loop == manager_loop:
            current_loop.create_task(coroutine)
        else:
            asyncio.run_coroutine_threadsafe(coroutine,manager_loop)


    def report_tool(
            self,
            tool_name:str,
            args:Optional[dict[str,Any]]=None,
    )->None:
        self._emit(
            "use_tool",
            f"开始执行工具:{tool_name}",
            {"tool_name":tool_name,"args":args}
        )

    def report_assistant(
            self,
            assistant_name:str,
            args:Optional[dict[str,Any]]=None
    )->None:
        self._emit(
            "assistant_call",
            f"正在调用助手:{assistant_name}",
            {"assistant_name":assistant_name,"args":args}
        )

    def report_task_result(
            self,
            result
    )->None:
        self._emit("task_result","任务执行完成",{"result":result})

    def report_task_cancelled(self)->None:
        self._emit("task_cancelled","任务已取消")

    def report_session_dir(self,path:str)->None:
        self._emit("session_created",f"工作目录已创建:{path}",{"path":path})



monitor = ToolMonitor()


class ConnectionManager:
    def __init__(self):
        self.active_connections:dict[str,WebSocket] = {}
        self.loop:Optional[asyncio.AbstractEventLoop] = None

    def set_loop(self,loop:asyncio.AbstractEventLoop)->None:
        self.loop = loop
        monitor.set_websocket_manager(self)
        print(f"[Monitor] ConnectionManager manually bound to loop:{id(self.loop)}")


    async def connect(self,websocket:WebSocket,thread_id:str)->None:
        await websocket.accept()
        self.active_connections[thread_id] = websocket
        print(f"Client connected:{thread_id}")


    def disconnect(self,websocket:WebSocket,thread_id:str)->None:
        if self.active_connections.get(thread_id) is websocket:
            del self.active_connections[thread_id]
            print(f"Client disconnect :{thread_id}")
        else:
            print(f"State websocket disconnected,current connection kept :{thread_id}")


    async def send_personal_message(self,message:str,websocket:WebSocket)->None:
        await websocket.send_text(message)


    async def send_to_thread(self,message:dict[str,Any],thread_id:str)->None:
        if thread_id in self.active_connections:
            websocket = self.active_connections[thread_id]
            await websocket.send_json(message)

manager = ConnectionManager()

















