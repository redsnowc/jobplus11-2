'''
配置文件，由四个类组成，基类存放共有配置项，开发、生产和测试类继承基类并适
应各自环境需求
'''

class BaseConfig:
    SECRET_KEY = 'SKLDJFASLKDJFKLSFJLSKDF;J'
    

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = (
            'mysql://root@localhost:3306/jobplus?charset=utf8')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
