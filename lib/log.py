# -*- coding: UTF-8 -*-
import logging
import sys
from conf.config import LOG_LEVEL


logger = logging.getLogger("dingding_notify")

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# formatter = logging.Formatter('[%(asctime)s] %(name)s %(levelname)s %(pathname)s %(lineno)d %(message)s')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

logger.setLevel(LOG_LEVEL)