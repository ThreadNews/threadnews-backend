import configparser
import logging
import os
import json

logger = logging.getLogger("root")


class threadConfiguration:
    """ gets configuration for program """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read_from_config_file()

    def read_from_config_file(self):
        """ reads configuration from file """

        if not os.path.exists(".config/api.conf"):
            if not os.path.exists(".config"):
                os.mkdir(".config")

            self.config.add_section("NewsAPI")
            self.config.add_section("MongoDB")
            self.config.add_section("JWT")

            """ read from environmental vars """
            if self.read_env_vars():
                logger.critical("no environmental variables found")
                config_file = open(".config/api.conf", "w")
                self.config.write(config_file)
                config_file.close()
                logger.critical("missing data/env vars, please add to .config/api.conf")
        else:
            """ only if configuration file is found """
            logger.info("configuration found")
            self.config.read(".config/api.conf")

    def read_env_vars(self):
        """reads off environmental vars

        Returns:
            boolean: true if all environmental vars are found
        """

        api_key = os.environ.get("NEWSAPIKEY")
        url = os.environ.get("MONGOURL")
        user = os.environ.get("MONGOUSER")
        password = os.environ.get("MONGOPASS")
        jwt_secret = os.environ.get("JWTSECRET")

        self.config.set("NewsAPI", "key", "YOURKEYHERE")
        if api_key:
            self.config.set("NewsAPI", "key", api_key)

        self.config.set("MongoDB", "URl", "YOURURLHERE")
        if url:
            self.config.set("MongoDB", "URl", url)

        self.config.set("MongoDB", "user", "YOURUSERHERE")
        if user:
            self.config.set("MongoDB", "user", user)

        self.config.set("MongoDB", "password", "YOURPASSWORDHERE")
        if password:
            self.config.set("MongoDB", "password", password)

        self.config.set("JWT", "secret", "YOURSECRETHERE")
        if jwt_secret:
            self.config.set("JWT", "secret", jwt_secret)

        return None in [api_key, url, user, password, jwt_secret]

    def get_configuration(self):
        """ returns the configuration file """
        return self.config

    def get_api_keys(self):
        """ gets the api key(s) """
        api_key = self.config["NewsAPI"]["key"]
        if "," in api_key:
            return [key.strip() for key in api_key.split(",")]
        else:
            return api_key
