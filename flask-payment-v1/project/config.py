import os


class BaseConfig:
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_DEV')
	pass


class TestingConfig(BaseConfig):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_TEST')


class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_PROD')
	pass
