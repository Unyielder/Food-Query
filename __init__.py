from flask import Flask
from .views import query


def create_app():
    app = Flask(__name__)

    app.register_blueprint(query)
    return app


if __name__ == '__main__':
    create_app()