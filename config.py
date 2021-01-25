import os

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SEND_FILE_MAX_AGE_DEFAULT = 0
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
