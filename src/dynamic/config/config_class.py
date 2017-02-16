import os


class ConfigClass():
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'mysql+pymysql://yassen:Streetfighter4@localhost/devmeter')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'groznika123@gmail.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        '3ee12ac0-f44a-11e6-9f88-e585862dca14')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  'DevMeter<groznika123@gmail.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'debugmail.io')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '25'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         False))

    # Flask-User settings
    USER_APP_NAME        = "DevMeter"                # Used by email templates