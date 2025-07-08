import json
import os
class ConfigReader:
    _config = None

    @staticmethod
    def load_config():
        if ConfigReader._config is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'testsetting.json')
            with open(config_path, 'r') as config_file:
                ConfigReader._config = json.load(config_file)
        return ConfigReader._config
    
    @staticmethod
    def get_base_url():
        return ConfigReader.load_config()['base_url']
    
    @staticmethod
    def get_implicit_timeout():
        return ConfigReader.load_config()['timeout']['implicit']

    @staticmethod
    def get_page_load_timeout():
        return ConfigReader.load_config()['timeout']['page_load']

    @staticmethod
    def get_username():
        return ConfigReader.load_config()['credentials']['username']
    
    @staticmethod
    def get_invalid_username():
        return ConfigReader.load_config()['credentials']['invalid_username']
    
    @staticmethod
    def get_blank_username():
        return ConfigReader.load_config()['credentials']['blank_username']
    @staticmethod
    def get_password():
        return ConfigReader.load_config()['credentials']['password']
    @staticmethod
    def get_invalid_password():
        return ConfigReader.load_config()['credentials']['invalid_password']
    @staticmethod
    def get_blank_password():
        return ConfigReader.load_config()['credentials']['blank_password']  