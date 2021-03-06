
from flask import Flask
from flask_uuid import FlaskUUID
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, Gitlab
from raven.contrib.flask import Sentry
import fatcat_client

from fatcat_web.web_config import Config

toolbar = DebugToolbarExtension()
app = Flask(__name__)
app.config.from_object(Config)
toolbar = DebugToolbarExtension(app)
FlaskUUID(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/auth/login"
oauth = OAuth(app)

# Grabs sentry config from SENTRY_DSN environment variable
sentry = Sentry(app)

conf = fatcat_client.Configuration()
conf.host = Config.FATCAT_API_HOST
api = fatcat_client.DefaultApi(fatcat_client.ApiClient(conf))

# remove most jinja2 template whitespace
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

def auth_api(token):
    conf = fatcat_client.Configuration()
    conf.api_key["Authorization"] = token
    conf.api_key_prefix["Authorization"] = "Bearer"
    conf.host = Config.FATCAT_API_HOST
    return fatcat_client.DefaultApi(fatcat_client.ApiClient(conf))

if Config.FATCAT_API_AUTH_TOKEN:
    print("Found and using privileged token (eg, for account signup)")
    priv_api = auth_api(Config.FATCAT_API_AUTH_TOKEN)
else:
    print("No privileged token found")
    priv_api = None

from fatcat_web import routes, auth, cors

gitlab_bp = create_flask_blueprint(Gitlab, oauth, auth.handle_oauth)
app.register_blueprint(gitlab_bp, url_prefix='/auth/gitlab')
