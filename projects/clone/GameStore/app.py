# implement design pattern where I will put all the application settings here

from flask import Flask
from auth.views import configure as config_auth
from auth.models import configure as config_db


from catalog.views import configure as config_catalog


def create_app(test_mode=False):
    # Initialize Flask framework
    app = Flask(__name__)

    # configuring views
    config_auth(app)

    config_catalog(app)

    # configuring bd
    config_db(app, test_mode)

    return app


# executes when we use python3 app.py in the terminal
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8080)
