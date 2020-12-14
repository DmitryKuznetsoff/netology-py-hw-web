from advertisement.views import advertisement
from app import app
from app.config import API_V1_URL_PREFIX
from user.views import users
from authtoken.views import authtoken

app.register_blueprint(users, url_prefix=API_V1_URL_PREFIX)
app.register_blueprint(authtoken, url_prefix=API_V1_URL_PREFIX)
app.register_blueprint(advertisement, url_prefix=API_V1_URL_PREFIX)
