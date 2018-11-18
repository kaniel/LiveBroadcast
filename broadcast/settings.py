import pytz


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_RECYCLE = 1800

    # For authentication
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'password-salt'
    # SECURITY_PASSWORD_DICT = "password_true"
    SECURITY_REGISTERABLE = False
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True

    ECURITY_EMAIL_SENDER = 'none@gmail.com'
    SECURITY_RESET_URL = '/api/auth/reset'
    SECURITY_RESET_PASSWORD_TEMPLATE = 'reset_password.html'
    SECURITY_CHANGE_URL = '/api/auth/change'
    SECURITY_UNAUTHORIZED_VIEW = 'auth.unauthorized'
    SECURITY_TOKEN_AUTHENTICATION_KEY = 'access_token'

    # Photos upload
    UPLOADED_PHOTOS_DEST = '/home/skill/uploads'
    UPLOADED_PHOTOS_URL = '/images/'

    WTF_CSRF_ENABLED = False
    # default client time zone
    DEFAULT_TIMEZONE = pytz.timezone('Asia/Shanghai')
    UTC_TIMEZONE = pytz.timezone('UTC')


class PROD(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:f4EBvtNFrDh4uAbb@rdsyqfyifaainjz.mysql.rds.aliyuncs.com/broadcastDB'
    # Receive email when error happens
    ADMINS = ['admin@skill.cn']
    LOGGING_PATH = '/home/skill/skill.log'
    LOGGING_SIZE = 10 * 1024 * 1024 # 10 mb


class DEV(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:234@localhost/broadcastDB'
    UPLOADED_PHOTOS_DEST = '/User/skill/uploads'

