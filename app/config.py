from celery import Celery, Task
from flask import Flask
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import os


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])

    celery_app.conf.update(
        result_expires=3600,
        timezone='UTC',
        beat_schedule={
            'getResult': {
                'task': 'app.tasks.getResults',
                'schedule': 10
            },
        },
    )
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    # Set up logging
    logger = logging.getLogger('celery')
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return celery_app

def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.getenv('CELERY_BROKER_URL'),
            result_backend=os.getenv('CELERY_BACKEND_URL'),
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app