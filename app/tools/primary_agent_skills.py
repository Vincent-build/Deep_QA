from langchain.tools import tool
from typing import Annotated,Optional
from api.context.context import get_session
from app.utils.path_utils import resolve_path
from app.utils.document_transform import transform_md_to_pdf
import os
from pathlib import Path
from base_config.logger.logger import logger
from api.monitor.monitor import monitor

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

try:
    import pandas as pd
except ImportError:
    pandas = None

@tool
def read_file_content(
        file_name:Annotated[str,"只支持文档格式(.md、.txt、.docx、.pdf、.xlsx、.xls)"],
        instruction:Annotated[str,"对提取内容的具体指令(例如：'提取摘要','统计数据')"]="提取全部内容",
):
    """
    读取用户上传的文档内容
    :param file_name: 文件路径或文件名
    :param instruction: 模型传入的读取意图，用于监控展示，不改变底层解析逻辑
    :return: 返回对应文件类型的内容，工具报错则返回报错内容
    """
    monitor.report_tool(tool_name="读取用户上传的文档:read_file_content",args={"instruction":instruction})
    session_dir = get_session()
    file_path = resolve_path(file_name,session_dir)

    if not file_path:
        return "文件名解析错误"

    ext = os.path.splitext(file_path)
    ext = ext[1]

    if ext in [".md",".txt"]:
        try:
            return Path(file_path).read_text(encoding='utf-8')
        except Exception as e:
            logger.error(str(e))
            return str(e)

    elif ext in [".docx"]:
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return "\n".join(full_text)
        except Exception as e:
            logger.error(str(e))
            return str(e)

    elif ext in [".pdf"]:
        try:
            reader = pypdf.PdfReader(file_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
            return text
        except Exception as e:
            logger.error(str(e))
            return str(e)


    elif ext in [".xlsx",'xls']:
        try:
            df = pd.read_excel(file_path)
            result = [
                f"文件:{file_name}",
                f"行数:{len(df)},列数:{len(df.columns)}",
                f"列名:{','.join(df.columns.astype(str))}",
                "\n{前5行数据预览}:",
                df.head().to_string(index=False),
                "\n[统计描述]:",
                df.describe().to_string(),
            ]
            return "\n".join(result)
        except Exception as e:
            logger.error(str(e))
            return str(e)

    else:
        try:
            return Path(file_name).read_text(encoding='utf-8')
        except Exception as e:
            logger.error(str(e))
            return str(e)



@tool
def generate_markdown(
        content:Annotated[str,"要写入Markdown文档的文本内容"],
        filename:Annotated[str,"Markdown文档的文件名,不包含扩展名或包含.md"],
):
    """
    根据提供的文本内容生成Markdown文本

    :param content: 要写入Markdown文档的完整文本
    :param filename: 输出文件名，缺少.md后缀时会自动补全
    :return: 文件生成结果说明
    """
    monitor.report_tool(tool_name="生成Markdown文档:generate_markdown")
    if not filename.endswith(".md"):
        filename += ".md"

    session_dir = get_session()

    try:
        full_path = resolve_path(str(Path(filename).name),session_dir)
        file_path = Path(full_path)

        parent_dir = file_path.parent

        if not parent_dir.exists():
            parent_dir.mkdir(parents=True,exist_ok=True)

        file_path.write_text(content,encoding='utf-8')
        logger.info(f"生成Markdown文件并保存于{file_path}")
        if file_path.exists():
            return f"Markdown文件'{file_path}'已成功生成并保存"
        else:
            return f"Markdown文件'{file_path}'未保存成功"
    except Exception as e:
        logger.error(str(e))
        return str(e)




@tool
def convert_md_to_pdf(
        md_filename:Annotated[str,"要转换的Markdown文档路径(包含.md后缀)"],
        pdf_filename:Annotated[Optional[str],"输出的PDF文件路径(可选，默认与原文件同名)"]
):
    """
    将当前会话目录中的Markdown文档转换成PDF
    :param md_filename: Markdown文件名或相对路径，缺少后缀时会自动补为.md
    :param pdf_filename: 可选PDF输出文件名；不传时与Markdown同名
    :return: 转换结果说明
    """
    monitor.report_tool("文档转换:convert_md_to_pdf")
    try:
        session_dir = get_session()
        file_path = resolve_path(str(Path(md_filename).with_suffix(".md")),session_dir)

        if pdf_filename:
            pdf_path = resolve_path(str(Path(pdf_filename).with_suffix(".pdf")),session_dir)
        else:
            pdf_path = str(Path(file_path).with_suffix(".pdf"))

        logger.info(f"生成pdf路径{pdf_path}，开始处理文档转换")
        result = transform_md_to_pdf(file_path,pdf_path)
        logger.info(f"{result}")
        return result
    except Exception as e:
        logger.error(str(e))
        return str(e)







if __name__ == "__main__":
    pass









