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


TOPIC_LIST = [
    "Architecture",
    "Remodeling",
    "DIY",
    "Garden stuff",
    "Pop Culture",
    "Music News",
    "Actors",
    "Tik Tok",
    "K Pop",
    "Economics",
    "Stocks",
    "Investing",
    "Budgeting",
    "Crypto",
    "Retirement",
    "Fitness",
    "Healthy Living",
    "Women's Health",
    "Mens Health",
    "Sports",
    "Pro Sports",
    "Beauty",
    "Cleansing",
    "Technology",
    "Startups",
    "Big Tech",
    "Programming",
    "Graphic Design",
    "Programming",
    "Graphic Design",
    "Sports",
    "Stocks",
    "Weather",
    "Skincare",
    "Cleansing",
    "Crypto",
    "Healthy Living",
    "DIY",
    "Freelancing",
    "Blogging",
    "K Pop",
    "Math",
]

