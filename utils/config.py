import configparser
import logging
import os

logger = logging.getLogger('root')

class threadConfiguration:
    def __init__(self):
        self.config = configparser.ConfigParser()
        if not os.path.exists(".config/api.conf"):
            if not os.path.exists(".config"):
                os.mkdir(".config")
            config_file = open(".config/api.conf", 'w')
            
            self.config.add_section('NewsAPI')
            self.config.add_section('MongoDB')
            self.config.add_section('JWT')

            self.config.set('NewsAPI', 'key', 'YOURKEYHERE')
            self.config.set('MongoDB', 'URl', 'YOURURLHERE')
            self.config.set('MongoDB', 'user', 'YOURUSERHERE')
            self.config.set('MongoDB', 'password', 'YOURPASSWORDHERE')
            self.config.set('JWT', 'secret', 'YOURSECRETHERE')
            self.config.write(config_file)
            config_file.close()

            logger.critical("missing data, please add key to .config/api.conf")
        self.config.read(".config/api.conf")
        
    def get_configuration(self):
        return self.config