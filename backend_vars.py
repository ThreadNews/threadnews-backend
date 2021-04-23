import utils.logger as logger
from utils.config import threadConfiguration
from utils.database import threadDatabase
from utils.feed import NewsAPICalls
from flask_apscheduler import APScheduler

log = logger.setup_logger('root')
configFile = threadConfiguration()
log.debug('initalized logger')

appFeed = NewsAPICalls(configFile.get_configuration())
database_client = threadDatabase(configFile.get_configuration())
scheduler = APScheduler()