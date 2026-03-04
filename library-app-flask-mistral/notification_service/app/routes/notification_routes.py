from flask import Blueprint
from flask_restx import Api
from app.controllers.notification_controller import api as notification_ns

notification_bp = Blueprint('notification', __name__)
api = Api(notification_bp, version='1.0', title='Notification Service API', description='Notification management')

api.add_namespace(notification_ns, path='/notifications')
