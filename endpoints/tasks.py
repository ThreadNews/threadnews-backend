from backend_vars import scheduler, log, appFeed

POLL_INTERVAL = 3600 #seconds

@scheduler.task('interval', id='feed_collector', seconds=POLL_INTERVAL)
def feed_worker():
   log.info("collecting articles")
   appFeed.begin_collection()

@scheduler.task('interval', id='test', seconds=5)
def test1():
   print("test 1")
