from flask import Flask, make_response, render_template, request, redirect, url_for, jsonify, session, send_file, abort
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
import json
from sqlalchemy import create_engine, not_, and_
from sqlalchemy.orm import Session
import os
import requests
import io
from datetime import datetime

from models import db, BaseTable, CustomerTable, ProfessionalTable, ServiceTable, AdminTable

from api_resources import *

from routes import *
#------------------------------------------------- Connections To Initialize -----------------------------------------------------------------------------


app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "Database/Project_DB.db")}'
app.config['SECRET_KEY'] = 'thesecretkey'

# Initialize SQLAlchemy with app
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

#------------------------------------------------- Secret Key -----------------------------------------------------------------------------

app.config['SECRET_KEY'] = 'thesecretkey'

#------------------------------------------------- API Endpoints -----------------------------------------------------------------------------

# Register API resource endpoints
api.add_resource(Professional_Service_Search_API, '/api/Professional_Service_Search')

api.add_resource(Customer_Summary_API, '/api/Customer_Summary')

api.add_resource(Professional_Summary_API, '/api/Professional_Summary')

api.add_resource(Professional_Today_Services_API, '/api/Professional_Today_Services')

api.add_resource(Professional_Closed_Services_API, '/api/Professional_Closed_Services')

api.add_resource(ServiceSummaryAPI, '/api/Service_Summary')

#------------------------------------------------- Routes -----------------------------------------------------------------------------

# Register all routes from routes.py
route_map = [
    ('/', Role_Selection, ['GET', 'POST']),
    ('/Customer_Login', Customer_Login, ['GET', 'POST']),
    ('/Admin_Login', Admin_Login, ['GET', 'POST']),
    ('/Professional_Login', Professional_Login, ['GET', 'POST']),
    ('/Customer_SignUp', Customer_SignUp, ['GET', 'POST']),
    ('/Professional_SignUp', Professional_SignUp, ['GET', 'POST']),
    ('/Customer_Home_Page', Customer_Home_Page, ['GET', 'POST']),
    ('/Professional_Home_Page', Professional_Home_Page, ['GET', 'POST']),
    ('/Admin_Home_Page', Admin_Home_Page, ['GET', 'POST']),
    ('/Professional_Profile', Professional_Profile, ['GET']),
    ('/Professional_Edit_Profile', Professional_Edit_Profile, ['GET', 'POST']),
    ('/Professional_Summary', Professional_Summary, ['GET']),
    ('/Admin_Summary', Admin_Summary, ['GET']),
    ('/Customer_Profile', Customer_Profile, ['GET']),
    ('/Customer_Edit_Profile', Customer_Edit_Profile, ['GET', 'POST']),
    ('/Customer_Search', Customer_Search, ['GET']),
    ('/Professional_Search', Professional_Search, ['GET']),
    ('/Admin_Search', Admin_Search, ['GET']),
    ('/Customer_Summary', Customer_Summary, ['GET']),
    ('/Close_Service/<int:service_id>', Close_Service, ['GET', 'POST']),
    ('/accept/<int:id>', Accept, ['GET']),
    ('/reject/<int:id>', Reject, ['GET']),
    ('/Add_Service', Add_Service, ['GET', 'POST']),
    ('/Edit_Service/<int:id>', Edit_Service, ['GET', 'POST']),
    ('/Delete_Service/<int:id>', Delete_Service, ['POST']),
    ('/Approve_Professional/<int:id>', Approve_Professional, ['POST']),
    ('/Reject_Professional/<int:id>', Reject_Professional, ['POST']),
    ('/Delete_Professional/<int:id>', Delete_Professional, ['POST']),
    ('/Download_Document/<int:professional_id>', Download_Document, ['GET']),
    ('/search', search_services, ['GET']),
    ('/api/services', get_services, ['GET']),
    ('/api/professionals/<service_name>', get_professionals, ['GET']),
    ('/Customer_Book/<int:professional_id>', Customer_Book, ['POST']),
    ('/api/service-history', get_service_history, ['GET']),
    ('/api/Professional_Service_Search', professional_service_search, ['GET']),
    ('/api/admin_summary', admin_summary, ['GET']),
    ('/api/search_service_summary', search_service_summary, ['GET']),
    ('/api/search_users', search_users, ['GET']),
    ('/api/toggle_block', toggle_block, ['POST']),
    ('/Logout', Logout, ['GET'])
]
for rule, view_func, methods in route_map:
    app.add_url_rule(rule, view_func=view_func, methods=methods)


if __name__ == '__main__':
    app.run(debug=True, port=8080)