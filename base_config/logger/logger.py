import logging
import colorlog
from pathlib import Path

path_ = Path(__file__).parents[2] / "app" / "log" / "dialog.log"
if not path_.exists():
    path_.mkdir(parents=True,exist_ok=True)



def logger(path):
    logger = logging.getLogger("Deepagent")
    logger.setLevel("INFO")
    if not logger.hasHandlers():
        filehandler = logging.FileHandler(path,encoding='utf-8')
        filehandler.setLevel("INFO")
        cmdhandler = logging.StreamHandler()
        cmdhandler.setLevel("INFO")
        template = colorlog.ColoredFormatter("%(log_color)s--%(levelname)s--%(name)s : %(message)s")
        filehandler.setFormatter(template)
        cmdhandler.setFormatter(template)
        logger.addHandler(filehandler)
        logger.addHandler(cmdhandler)
    return logger

logger = logger(path_)

if __name__ == "__main__":
    logger.info("你好，这是")










