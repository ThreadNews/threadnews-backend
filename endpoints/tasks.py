from backend_vars import scheduler, log, appFeed, database_client


# @scheduler.task('interval', id='feed_collector', seconds=POLL_INTERVAL)
def feed_worker():
    log.info("collecting articles")
    database_client.push_new_articles(appFeed.begin_collection())
