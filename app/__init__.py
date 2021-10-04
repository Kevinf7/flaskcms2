from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.breadcrumb import Breadcrumb
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
# compare_type = true - this is so that flask migrate detect changes to columns like size
migrate = Migrate(compare_type=True)
moment = Moment()
login_manager = LoginManager()
breadcrumb = Breadcrumb()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app,db)
        moment.init_app(app)
        csrf.init_app(app)

        from app.admin_auth import bp as admin_auth_bp
        app.register_blueprint(admin_auth_bp, url_prefix='/admin')

        from app.admin_main import bp as admin_main_bp
        app.register_blueprint(admin_main_bp, url_prefix='/admin')
        
        if app.config['ADMIN_BLOG']:
            from app.admin_blog import bp as admin_blog_bp
            app.register_blueprint(admin_blog_bp, url_prefix='/admin')

        if app.config['ADMIN_MESSAGE']:
            from app.admin_message import bp as admin_message_bp
            app.register_blueprint(admin_message_bp, url_prefix='/admin')

        if app.config['ADMIN_PAGE']:
            from app.admin_page import bp as admin_page_bp
            app.register_blueprint(admin_page_bp, url_prefix='/admin')

        if app.config['ADMIN_BLOG'] or app.config['ADMIN_PAGE']:
            from app.admin_media import bp as admin_media_bp
            app.register_blueprint(admin_media_bp, url_prefix='/admin')

        if app.config['ADMIN_SHOP']:
            from app.admin_shop import bp as admin_shop_bp
            app.register_blueprint(admin_shop_bp, url_prefix='/admin')

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)
        
        from app.email import bp as email_bp
        app.register_blueprint(email_bp)

        from app.sitemap import bp as sitemap_bp
        app.register_blueprint(sitemap_bp)

        breadcrumb.init_app(app)

        # if not app.debug:
        folder = app.config['BASEDIR'] / 'logs'
        if not folder.is_dir():
            folder.mkdir()
        file_handler = RotatingFileHandler(folder / 'flask_cms.log', maxBytes=10240,
            backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask startup')

        # Set rest of config from db
        # Please comment this out when first creating database tables
        set_settings()

    return app

from app.admin_main.settings import set_settings