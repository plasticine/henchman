from os import path
import logging
from ..settings import settings


log = logging.getLogger('henchman')
log.setLevel(logging.DEBUG)

# file based logs
logfilename = path.join(settings.logs_root, 'henchman.log')
filelog = logging.FileHandler(logfilename, 'a')
filelog.setLevel(logging.INFO)

# Use console for development logging:
conlog = logging.StreamHandler()
conlog.setLevel(logging.DEBUG)

# Specify log formatting:
formatter = logging.Formatter("%(asctime)s - %(name)s - %(lineno)s - \
%(levelname)s - %(message)s")
conlog.setFormatter(formatter)
filelog.setFormatter(formatter)

# Add console log to logger
log.addHandler(conlog)
log.addHandler(filelog)
