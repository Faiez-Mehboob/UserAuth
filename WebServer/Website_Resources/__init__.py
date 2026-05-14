from flask import Flask

def create_app(AuthHOST='localhost',AuthPORT=9999):
    app = Flask(__name__)
    app.config['SECRET_KEY']='mysecretkey'
    app.config['AuthHOST']=AuthHOST
    app.config['AuthPORT']=AuthPORT
    
    from .auth import auth
    from .dash import dash
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(dash, url_prefix='/')

    return app