from contextvars import ContextVar,Token
from typing import Optional

_session_dir_ctx:ContextVar[Optional[str]] = ContextVar(
    "session_dir",
    default=None
)

_thread_id_ctx:ContextVar[Optional[str]] = ContextVar(
    "thread_id",
    default=None
)


def set_session(path:str)->Token[Optional[str]]:
    return _session_dir_ctx.set(path)


def get_session()->Optional[str]:
    return _session_dir_ctx.get()

def set_thread(path:str)->Token[Optional[str]]:
    return _thread_id_ctx.set(path)


def get_thread()->Optional[str]:
    return _thread_id_ctx.get()


def reset_context(session_id:Token[Optional[str]],thread_id:Optional[Token[Optional[str]]]=None):
    _session_dir_ctx.reset(session_id)
    if thread_id is not None:
        _thread_id_ctx.reset(thread_id)








