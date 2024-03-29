import utils.logger as logger
from utils.config import threadConfiguration
from utils.database import threadDatabase
from utils.feed import NewsAPI

# from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

log = logger.setup_logger("root")
configFile = threadConfiguration()
log.debug("initalized logger")

database_client = threadDatabase(configFile.get_configuration())
appFeed = NewsAPI(configFile)
# scheduler = APScheduler()
scheduler = BackgroundScheduler()
