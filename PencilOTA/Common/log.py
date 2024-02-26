# -*-coding:utf-8 -*-
import logging
import time

from PencilOTA.Common.utils import get_phone_time


class Logger:

    def __init__(self, logger, FilePath, device, CmdLevel=logging.INFO, FileLevel=logging.INFO):
        self.logger = logging.getLogger(logger)
        # 设置日志输出的默认级别
        self.logger.setLevel(logging.DEBUG)
        self.device = device
        self.time_value = str(
            get_phone_time(device=device) + '- %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        self.fmt = logging.Formatter(self.time_value)
        currentTime = time.strftime("%Y-%m-%d-%H-%M-%S")
        self.logFileName = FilePath + '\\' + currentTime + ".log"
        self.Fl = FileLevel
        # 文件输出到磁盘中
        self.fh = logging.FileHandler(self.logFileName)

    def style_set(self):
        self.time_value = str(
            get_phone_time(device=self.device) + '- %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        self.fmt = logging.Formatter(self.time_value)
        self.fh.setFormatter(self.fmt)
        self.fh.setLevel(self.Fl)
        self.logger.addHandler(self.fh)

    def debug(self, msg):
        self.style_set()
        self.logger.debug(msg)

    def info(self, msg):
        self.style_set()
        self.logger.info(msg)

    def warn(self, msg):
        self.style_set()
        self.logger.warning(msg)

    def error(self, msg):
        self.style_set()
        self.logger.error(msg)

    def critical(self, msg):
        self.style_set()
        self.logger.critical(msg)


if __name__ == '__main__':
    logger = Logger("fox", device="AMABUN3925H00005", FilePath='D:\work\PC006主动笔\\tool_log')

    for i in [1, 2, 3]:
        logger.info("第{}次".format(i))
        time.sleep(2)
