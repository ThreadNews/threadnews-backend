from backend_vars import scheduler, log, appFeed, database_client


test_user_ids = [
    "a49387e4-7c51-11eb-95d3-acde48001122",
    "e269cc10-a34b-11eb-92dd-acde48001122",
    "0e7bf4b8-7c28-11eb-95d3-acde48001122",
    "1e0a2610-a672-11eb-a5a6-acde48001122",
]


# @scheduler.task('interval', id='test_users_likes', seconds=500000)
def test_users_actions():

    for user_id in test_user_ids:
        article = database_client.get_random_article()
        # like article
        database_client.add_likes_articles(user_id=user_id, article_id=article["id"])

        article = database_client.get_random_article()
        # share article
        database_client.repost_article(user_id=user_id, article_id=article["id"])


# @scheduler.task('interval', id='feed_collector', seconds=POLL_INTERVAL)
def feed_worker():
    log.info("collecting articles")
    database_client.push_new_articles(appFeed.begin_collection())
