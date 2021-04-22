import logger
from config import threadConfiguration
from database import threadDatabase
from feed import NewsAPICalls
from flask_apscheduler import APScheduler

log = logger.setup_logger('root')
configFile = threadConfiguration()
log.debug('initalized logger')

appFeed = NewsAPICalls(configFile.get_configuration())
database_client = threadDatabase(configFile.get_configuration())
scheduler = APScheduler()