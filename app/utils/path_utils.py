"""
路径统一解析：清洗虚拟路径、识别上传目录、拼接当前会话目录
"""
from pathlib import Path
import os
from typing import Union,Optional,Annotated


def resolve_path(filename:Annotated[Union[str,Path],"传入的文件路径，包含文件后缀名"],session_dir:Optional[str]=None):
    origin_store = Path(__file__).parents[2] / "save_dir"
    output_store = Path(__file__).parents[2] / "save_dir" / "output"
    virtual_path = ["/workspace","/mnt/data","/home/user","/private/tmp/workspace","/private_documents"]
    file_path = filename
    for path in virtual_path:
        if filename.startswith(path):
            file_path = filename[len(path):].lstrip("/")
            break


    if not session_dir:
        path = str(Path(file_path))
        path_whole = os.path.join(str(origin_store),path)
        return str(Path(path_whole).resolve())


    if file_path.startswith(session_dir):
        path = os.path.join(output_store,file_path)
        return str(Path(path).resolve())


    if "updated/" in file_path:
        index = file_path.find("updated/")
        file_path = file_path[index:]
        path = os.path.join(origin_store,file_path)
        return str(Path(path).resolve())

    if "output/session" in file_path:
        index = file_path.find("output/")
        file_path = file_path[index:]
        path = os.path.join(origin_store, file_path)
        return str(Path(path).resolve())


    if (os.name == "posix" and os.path.isabs(file_path) and file_path.startswith("/Users")) or (not file_path.startswith("/Users") and os.name == "posix"):
        if not file_path.startswith("/Users") and os.name == "posix":
            path = output_store / f"{session_dir}" / file_path.lstrip("/")
            return str(path)
        else:
            project_dir = Path(__file__).parents[2]

            path = Path(file_path).resolve()
            session_name = Path(session_dir).resolve().name
            path_parts = path.parts

            if session_name in path_parts:
                for index in range(len(path_parts) - 1):
                    if path_parts[index] == path_parts[index + 1]:
                        path = output_store / f"session_{session_dir}" / str(Path(file_path).name)
                        break

            if not path.is_relative_to(project_dir):
                if session_name in path_parts:
                    path = output_store / f"session_{session_dir}" / str(Path(file_path).name)
                else:
                    path = origin_store / str(Path(file_path).name)
            else:
                if session_name in path_parts:
                    path = output_store / f"session_{session_dir}" / str(Path(file_path).name)

            return str(path)



if __name__ == "__main__":
    r = resolve_path("/Source_code/D_Agent/session_123/kinder/ming.md","session_123")




































