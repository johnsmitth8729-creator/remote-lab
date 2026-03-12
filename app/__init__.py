from flask import Flask, request, redirect, make_response
from .config import Config
from .extensions import db, jwt, bcrypt, migrate, babel
import os

from flask_jwt_extended import get_jwt_identity, get_jwt

def get_locale():
    # Priority: 1. Cookie 'lang', 2. Browser Accept-Language, 3. Default 'en'
    cookie_lang = request.cookies.get('lang')
    if cookie_lang in ['en', 'uz', 'ru']:
        return cookie_lang
    return request.accept_languages.best_match(['en', 'uz', 'ru']) or 'en'

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)
    
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        from flask import flash, redirect, url_for
        flash('Siz ushbu sahifani ko\'rish uchun tizimga kirishingiz kerak.', 'warning')
        return redirect(url_for('auth.login'))

    @app.context_processor
    def inject_globals():
        from flask_jwt_extended import verify_jwt_in_request
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            pass
        return dict(
            get_locale=get_locale,
            get_jwt_identity=get_jwt_identity,
            get_jwt=get_jwt
        )

    # Register Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.experiment_routes import experiment_bp
    from .routes.user_routes import user_bp
    from .routes.admin_routes import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(experiment_bp, url_prefix='/api/experiments')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    @app.route('/set_language/<lang>')
    def set_language(lang):
        next_url = request.referrer or '/'
        if lang not in ['en', 'uz', 'ru']:
            lang = 'en'
        resp = make_response(redirect(next_url))
        resp.set_cookie('lang', lang, max_age=60*60*24*365) # 1 year
        return resp

    # Global Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        from flask import render_template
        return render_template('500.html'), 500

    return app
