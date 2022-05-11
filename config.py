import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_type = 'sqlite'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = False  # true = log all statements

    if db_type == 'sqlite':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                  'sqlite:///' + os.path.join(basedir, 'app.db')


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False  # true = log all statements
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'mssql://DESKTOP-DB7OB87\SQLPMH/CRUD?driver=SQL+Server'

    # sqlite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

