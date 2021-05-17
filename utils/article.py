import uuid


class Article:
    @staticmethod
    def convertToDataFrame(article_data):
        def convertor(article):
            unique_bytes = ""
            if article["author"]:
                unique_bytes += article["author"]
            if article["title"]:
                unique_bytes += article["title"]
            if article["url"]:
                unique_bytes += article["url"]
            article["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_bytes))
            article["global_score"] = 50
            article["main_topic"] = ""
            article["tags"] = {}
            return article

        if isinstance(article_data, list):
            return [convertor(article) for article in article_data]
        return [convertor(article_data)]
