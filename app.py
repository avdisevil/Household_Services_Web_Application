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

#------------------------------------------------- Connections To Initialize -----------------------------------------------------------------------------

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "Database/Project_DB.db")}'
db = SQLAlchemy(app)
app.app_context().push()

#------------------------------------------------- Secret Key -----------------------------------------------------------------------------

app.config['SECRET_KEY'] = 'thesecretkey'

#------------------------------------------------- APIs -----------------------------------------------------------------------------

#   API For Adding Customer Details
class Customer_Registration_API(Resource):
    def post(self, data):
        required_fields = ['email_id', 'password', 'full_name', 'address', 'pincode']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        email_check = CustomerTable.query.filter_by(email_id = data['email_id']).first()
        
        if email_check:
            return {"error": "This email is linked to an already existing Customer"}, 400

        New_Customer = CustomerTable(
            email_id = data['email_id'],
            password = data['password'],
            full_name = data['full_name'],
            address = data['address'],
            pin_code = data['pincode']
        )

        db.session.add(New_Customer)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 200

#   API For Customer Login Verification
class Customer_Login_API(Resource):
    def post(self, data):
        required_fields = ['email_id', 'password']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400
        
        customer = CustomerTable.query.filter_by(email_id = data['email_id']).first()
        if not customer:
            return {"error": "Customer not found"}, 404

        if customer.password != data['password']:
            return {"error": "Incorrect password"}, 401

        return {"message": "Login successful!", "customer_id": customer.customer_id}, 200
    
#   API For Professional Login Verification
class Professional_Login_API(Resource):
    def post(self, data):
        required_fields = ['email_id', 'password']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400
        
        professional = ProfessionalTable.query.filter_by(email_id = data['email_id']).first()
        if not professional:
            return {"error": "Professional not found"}, 404

        if professional.password != data['password']:
            return {"error": "Incorrect password"}, 401

        return {"message": "Login successful!", "professional_id": professional.professional_id}, 200
    
#   API For Admin Login Verification
class Admin_Login_API(Resource):
    def post(self, data):
        required_fields = ['email_id', 'password']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400
        
        admin = AdminTable.query.filter_by(email_id = data['email_id']).first()
        if not admin:
            return {"error": "Admin not found"}, 404

        if admin.password != data['password']:
            return {"error": "Incorrect password"}, 401

        return {"message": "Login successful!", "admin_id": admin.admin_id}, 200

#   API For Customer Profile Details
class Customer_Profile_API(Resource):
    def get(self, customer_id):
        customer = CustomerTable.query.filter(CustomerTable.customer_id == customer_id).first()        
        if customer:
            return {
                "customer_id": customer.customer_id,
                "email_id": customer.email_id,
                "full_name": customer.full_name,
                "address": customer.address,
                "pin_code": customer.pin_code
            }, 200
        else:
            return {"error": "Customer not found"}, 404
    
    def put(self, data):
        customer = CustomerTable.query.get(data['customer_id'])
        if customer:
            customer.full_name = data['full_name']
            customer.address = data['address']
            customer.pin_code = data['pin_code']
            db.session.commit()

            return {"message": "Customer profile updated successfully."}, 200
        else:
            return {"message": "Customer not found."}, 404
        
#   API For Professional Profile Details
class Professional_Profile_API(Resource):
    def get(self, professional_id):
        professional = ProfessionalTable.query.filter(ProfessionalTable.professional_id == professional_id).first()        
        if professional:
            return {
                "professional_id": professional.professional_id,
                "email_id": professional.email_id,
                "full_name": professional.full_name,
                "address": professional.address,
                "pin_code": professional.pin_code,
                "experience": professional.experience,
                "description": professional.description,
                "rating": professional.rating
            }, 200
        else:
            return {"error": "Professional not found"}, 404
        
    def put(self, data):
        professional = ProfessionalTable.query.filter(ProfessionalTable.professional_id == data['professional_id']).first()        
        if professional:
            professional.full_name = data['full_name']
            professional.address = data['address']
            professional.pin_code = data['pin_code']
            professional.experience = data['experience']
            professional.description = data['description']
            
            db.session.commit()
            return {"message": "Professional Details Updated Successfully"}, 200
        else:
            return {"error": "Professional Not Found"}, 404

#   API For Services (Display, Delete, Update, Create)
class Services_API(Resource):
    def get(self):
        services = ServiceTable.query.all()
        if services:
            services_list = [{
                'id': service.id,
                'name': service.name,
                'price': service.price,
                'time_required': service.time_required,
                'description': service.description
            } for service in services]
            return {'services': services_list}, 200
        else:
            return {'message': 'No services found.'}, 404
    
    def post(self, data):
        new_service = ServiceTable(
            name = data['name'],
            price = data['price'],
            time_required = data['time_required'],
            description = data['description']
        )

        service_check = ServiceTable.query.filter_by(name = data['name']).first()

        if service_check:
            return {"error": "This Service Already Exists"}, 400
        
        db.session.add(new_service)
        db.session.commit()

        return {"message": "Service Created Successfully"}, 200
    
    def put(self, data):
        service = ServiceTable.query.get(data['id'])
        if service:
            service.name = data['name']
            service.price = data['price']
            service.time_required = data['time_required']
            service.description = data['description']
            db.session.commit()

            return {"message": "Service updated successfully."}, 200
        else:
            return {"message": "Service not found."}, 404

    def delete(self, data):
        service = ServiceTable.query.get(data['id'])
        if service:
            db.session.delete(service)
            db.session.commit()

            return {"message": "Service deleted successfully."}, 200
        else:
            return {"error": "Service not found."}, 404

#   API For Getting All Professional Details
class Professional_API(Resource):
    def get(self):
        professionals = ProfessionalTable.query.filter(ProfessionalTable.approve == 0).all()

        if professionals:
            professional_list = []
            for professional in professionals:
                professional_data = {
                    "professional_id": professional.professional_id,
                    "email_id": professional.email_id,
                    "full_name": professional.full_name,
                    "service_name": professional.service_name,
                    "experience": professional.experience,
                    "document": professional.document,
                    "address": professional.address,
                    "pin_code": professional.pin_code,
                    "description": professional.description,
                    "approve": professional.approve,
                    "rating": professional.rating
                }
                professional_list.append(professional_data)
            
            return {'professional_list': professional_list}, 200
        
        else:
            return {'professional_list': []}, 200
        
    def delete(self, professional_id):
        professional = ProfessionalTable.query.get(professional_id)

        if professional:
            db.session.delete(professional)
            db.session.commit()

            return {'message': "Professional Deleted Successfully"}, 200
        
        else:
            return {'error': "No Professional Found"}, 404
        
    def put(self, data):
        professional = ProfessionalTable.query.get(data['professional_id'])

        if professional:
            if data['case'] == 1:
                professional.approve = 1
                
            else:
                professional.approve = 0

            db.session.commit()
            return {'message': "Professional Has Been Approved"}, 200
        
        else:
            return {'error': "No Professional Found"}, 404
        
    def post(self, data):
        required_fields = ['email_id', 'password', 'full_name', 'address', 'pincode', 'service_name', 'experience', 'document', 'description']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        email_check = ProfessionalTable.query.filter_by(email_id = data['email_id']).first()
        
        if email_check:
            return {"error": "This email is linked to an already existing Professional"}, 400

        New_Professional = ProfessionalTable(
            email_id=data['email_id'],
            password=data['password'],
            full_name=data['full_name'],
            address=data['address'],
            pin_code=data['pincode'],
            service_name=data['service_name'],
            experience=data['experience'],
            document=data['document'],
            description=data['description']
        )

        db.session.add(New_Professional)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 200

#   API For Closing A Service
class Close_Service_API(Resource):
    def put(self, data):
        service = BaseTable.query.filter(BaseTable.id == data['service_id']).first()

        if service:
            service.service_status = 0
            service.date_of_completion = datetime.now().date()
            service.remarks = data['remarks']
            service.service_rating = data['rating']

            professional_id = service.professional_id

            db.session.commit()

            professional = ProfessionalTable.query.filter(ProfessionalTable.professional_id == professional_id).first()
            professional.rating = (data['rating'] + professional.rating) / 2

            db.session.commit()

            return {"message": "Service Closed Successfully"}, 200
        
        else:
            return {"error": "No Such Service Available"}, 404

#   API For Creating Customer Summary
class Customer_Summary_API(Resource):
    def get(self):
        
        customer_id = session.get('customer_id')
        assigned = BaseTable.query.filter(BaseTable.service_status == 2, BaseTable.customer_id == customer_id).count()
        closed = BaseTable.query.filter(BaseTable.service_status == 0, BaseTable.customer_id == customer_id).count()
        requested = BaseTable.query.filter(BaseTable.service_status == 1, BaseTable.customer_id == customer_id).count()

        if customer_id:
            return {'assigned': assigned, 'closed': closed, 'requested': requested}, 200
        
        else:
            return {'error': 'No Customer Logged In'}, 401

#   API For Creating Professional Summary
class Professional_Summary_API(Resource):
    def get(self):
        
        professional_id = session.get('professional_id')
        assigned = BaseTable.query.filter(BaseTable.service_status == 2, BaseTable.professional_id == professional_id).count()
        closed = BaseTable.query.filter(BaseTable.service_status == 0, BaseTable.professional_id == professional_id).count()
        requested = BaseTable.query.filter(BaseTable.service_status == 1, BaseTable.professional_id == professional_id).count()

        if professional_id:
            return {'assigned': assigned, 'closed': closed, 'requested': requested}, 200
        
        else:
            return {'error': 'No Professional Logged In'}, 401


# API For Searching Services - Only Closed Services (service_status == 0)
class Professional_Service_Search_API(Resource):
    def get(self):
        # Extract the search criteria from request arguments
        search_by = request.args.get('by')
        search_text = request.args.get('text')
        professional_id = session.get('professional_id')

        if not professional_id:
            return {'error': 'No Professional Logged In'}, 401

        # Base query for closed services
        query = BaseTable.query.filter(BaseTable.service_status == 0, BaseTable.professional_id == professional_id)

        # Apply filters based on search criteria
        if search_by == 'address':
            query = query.filter(ProfessionalTable.address.ilike(f'%{search_text}%'))
        elif search_by == 'pincode':
            query = query.filter(ProfessionalTable.pin_code == search_text)
        elif search_by == 'date_of_completion':
            query = query.filter(BaseTable.date_of_completion == search_text)

        # Perform the query and fetch results
        results = query.join(CustomerTable, BaseTable.customer_id == CustomerTable.id).all()

        # Prepare the response data
        response_data = []
        for service in results:
            response_data.append({
                'id': service.id,
                'customer_name': service.customer.full_name,
                'location': service.customer.address,
                'pin_code': service.customer.pin_code,
                'date_of_completion': service.date_of_completion.strftime('%Y-%m-%d'),
                'rating': service.service_rating,
            })

        return response_data, 200

#To Display All The Services Present In Base Table
class ServiceSummaryAPI(Resource):  
    def get(self):
        # Query to join the tables and get the necessary data
        services = (
            db.session.query(
                BaseTable.id,
                BaseTable.date_of_request,
                BaseTable.service_status,
                CustomerTable.full_name.label('customer_name'),
                ProfessionalTable.full_name.label('professional_name')
            )
            .join(CustomerTable, BaseTable.customer_id == CustomerTable.customer_id)
            .outerjoin(ProfessionalTable, BaseTable.professional_id == ProfessionalTable.professional_id)
            .all()
        )
        
        # Creating the response list
        service_list = []
        STATUS_MAPPING = {
            0: "Closed",
            1: "Requested",
            2: "Accepted"
        } 
        for service in services:
            service_data = {
                "ID": service.id,
                "Professional Name": service.professional_name if service.professional_name else "N/A",
                "Requested Date": service.date_of_request.strftime('%Y-%m-%d'),
                "Customer Name": service.customer_name,
                "Status": STATUS_MAPPING.get(service.service_status, "Unknown")
            }
            service_list.append(service_data)

        return jsonify(service_list)
    
#   API For Displaying Today's Services
class Professional_Today_Services_API(Resource):
    def get(self):
        professional_id = session.get('professional_id')
        
        services = BaseTable.query.filter(BaseTable.professional_id == professional_id, BaseTable.service_status == 1).all()
        if services:
            service_list = []
            for service in services:
                customer_id = service.customer_id
                customer = CustomerTable.query.filter(CustomerTable.customer_id == customer_id).first()
                data = {
                    'id': service.id,
                    'full_name': customer.full_name,
                    'address': customer.address,
                    'pin_code': customer.pin_code
                }
                service_list.append(data)


            return {"service_list": service_list}, 200

        else:
            return {"service_list": []}, 200

#   API For Displaying Closed Services By Professional
class Professional_Closed_Services_API(Resource):
    def get(self):
        professional_id = session.get('professional_id')
        
        services = BaseTable.query.filter(BaseTable.professional_id == professional_id, BaseTable.service_status == 0).all()
        if services:
            service_list = []
            for service in services:
                customer_id = service.customer_id
                customer = CustomerTable.query.filter(CustomerTable.customer_id == customer_id).first()
                date_of_completion_str = service.date_of_completion.strftime('%Y-%m-%d') if service.date_of_completion else None
                data = {
                    'id': service.id,
                    'full_name': customer.full_name,
                    'address': customer.address,
                    'pin_code': customer.pin_code,
                    'date_of_completion': date_of_completion_str,
                    'service_rating': service.service_rating
                }
                service_list.append(data)


            return {"service_list": service_list}, 200

        else:
            return {"service_list": []}, 200
        
#   API For Accepting / Rejecting Request From Customer
class Professional_Accept_Reject_API(Resource):
    def put(self, data):
        if data['case'] == 1:
            service = BaseTable.query.filter(BaseTable.id == data['id']).first()
            if service:
                service.service_status = 2

                db.session.commit()
                return {"message": "Service Has Been Assigned Successfully"}, 200
            else:
                return {"error": "No Such Service Found"}, 404
            
        elif data['case'] == 0:
            service = BaseTable.query.filter(BaseTable.id == data['id']).first()
            if service:
                db.session.delete(service)

                db.session.commit()
                return {"message": "Service Has Been Assigned Successfully"}, 200
            else:
                return {"error": "No Such Service Found"}, 404
            
        else:
            return {"error": "Case Should Be Either 0 Or 1"}, 400

#   API For Checking If Customer Is Blocked
class Check_Block_Customer_API(Resource):
    def get(self):
        customer_id = session.get('customer_id')
        
        if not customer_id:
            return {"message": "Customer not logged in"}, 401

        customer = CustomerTable.query.filter(
            CustomerTable.customer_id == customer_id,
            CustomerTable.block == 0
        ).first()

        if customer:
            return {"is_blocked": 0}, 200
        else:
            return {"is_blocked": 1}, 200

#   API For Checking If Professional Is Blocked
class Check_Block_Professional_API(Resource):
    def get(self):
        professional_id = session.get('professional_id')
        
        if not professional_id:
            return {"message": "Professional not logged in"}, 401

        professional = ProfessionalTable.query.filter(
            ProfessionalTable.professional_id == professional_id,
            ProfessionalTable.block == 0
        ).first()

        if professional:
            return {"is_blocked": 0}, 200
        else:
            return {"is_blocked": 1}, 200


#   To Get All The Services Being Searched By Customer
@app.route('/search', methods=['GET'])
def search_services():
    # Get query parameters
    search_by = request.args.get('by')
    search_text = request.args.get('text')
    customer_id = session.get('customer_id')

    # Initialize query based on search criteria
    query = db.session.query(ServiceTable, ProfessionalTable).select_from(ServiceTable).join(
        ProfessionalTable, ServiceTable.name == ProfessionalTable.service_name
    ).outerjoin(BaseTable, 
        (BaseTable.service_id == ServiceTable.id) & 
        (BaseTable.customer_id == customer_id) & 
        (BaseTable.professional_id == ProfessionalTable.professional_id) & 
        (BaseTable.service_status.in_([1, 2]))  # Filter out services already booked with status 1 or 2
    ).filter(
        ProfessionalTable.block == 0,
        ProfessionalTable.approve == 1,  # Filter for approved professionals
        BaseTable.id == None  # Ensure we only get services not booked by the customer
    )

    if search_by == "service_name":
        # Search by service name, using case-insensitive matching
        results = query.filter(ServiceTable.name.ilike(f"%{search_text}%")).all()
    elif search_by == "pincode":
        # Search by pincode (integer type)
        try:
            pincode = int(search_text)
            results = query.filter(ProfessionalTable.pin_code == pincode).all()
        except ValueError:
            return jsonify({"error": "Pincode must be a number"}), 400
    elif search_by == "experience":
        # Search by experience (integer type)
        try:
            experience_years = int(search_text)
            results = query.filter(ProfessionalTable.experience >= experience_years).all()
        except ValueError:
            return jsonify({"error": "Experience must be a number"}), 400
    else:
        return jsonify({"error": "Invalid search criteria"}), 400

    # Format the results as a list of dictionaries
    services = []
    for service, professional in results:
        services.append({
            "id": professional.professional_id,  # Assuming this is the correct ID for the professional
            'full_name': professional.full_name,
            "description": professional.description,  # Use the correct description
            "base_price": service.price,
            "rating": professional.rating,
        })

    # Return the formatted results
    return jsonify(services), 200

#   To Get All Service Names
@app.route('/api/services', methods=['GET'])
def get_services():
    services = ServiceTable.query.all()
    return jsonify([{'name': service.name} for service in services])

#   To Get All Professionals Of A Particular Service
@app.route('/api/professionals/<service_name>', methods=['GET'])
def get_professionals(service_name):
    customer_id = session.get('customer_id')
    
    if not customer_id:
        return jsonify({"error": "Customer not authenticated"}), 401
    
    excluded_professionals = (
        db.session.query(BaseTable.professional_id)
        .filter(
            BaseTable.customer_id == customer_id,
            BaseTable.service_status.in_([1, 2])
        )
    )

    professionals = ProfessionalTable.query.filter(
        ProfessionalTable.service_name == service_name,
        ProfessionalTable.approve == 1,
        ProfessionalTable.block == 0,
        not_(ProfessionalTable.professional_id.in_(excluded_professionals))
    ).all()
    
    if not professionals:
        return jsonify([])

    return jsonify([
    {
        'professional_id': professional.professional_id,
        'full_name': professional.full_name,
        'experience': professional.experience,
        'rating': professional.rating,
        'description': professional.description
    } 
    for professional in professionals
])

#   Customer Booking A Professional
@app.route('/Customer_Book/<int:professional_id>', methods=['POST'])
def Customer_Book(professional_id):

    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({'message': 'User not logged in'}), 401

    professional = ProfessionalTable.query.filter_by(professional_id=professional_id).first()
    if not professional:
        return jsonify({'message': 'Professional not found'}), 404

    service = ServiceTable.query.filter_by(name=professional.service_name).first()
    if not service:
        return jsonify({'message': 'Service not found'}), 404

    booking = BaseTable(
        service_id=service.id,
        customer_id=customer_id,
        professional_id=professional_id,
        date_of_request=datetime.today().date(),
        service_status=1
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking successful'})

#   Customer Service History
@app.route('/api/service-history', methods=['GET'])
def get_service_history():
    user_id = session.get('customer_id')

    # Querying the service history
    service_history = (
        db.session.query(BaseTable.id, ServiceTable.name.label('service_name'), 
                         ProfessionalTable.full_name.label('professional_name'), 
                         BaseTable.service_status)
        .join(ServiceTable, BaseTable.service_id == ServiceTable.id)
        .join(ProfessionalTable, BaseTable.professional_id == ProfessionalTable.professional_id)
        .filter(BaseTable.customer_id == user_id)  # Filter by the current user's ID
        .all()
    )

    # Formatting the response
    response = []
    for record in service_history:
        response.append({
            'id': record.id,
            'service_name': record.service_name,
            'professional_name': record.professional_name,
            'service_status': record.service_status
        })
    
    return jsonify(response)

#   Professional Searching Through Service History
@app.route('/api/Professional_Service_Search') 
def professional_service_search():
    search_by = request.args.get('by')
    search_text = request.args.get('text')

    professional_id = session.get('professional_id')
    
    query = BaseTable.query.join(CustomerTable, BaseTable.professional_id == professional_id).filter(BaseTable.customer_id == CustomerTable.customer_id)
    
    if search_by == 'address':
        query = query.filter(CustomerTable.address.ilike(f"%{search_text}%"))
    elif search_by == 'pincode':
        query = query.filter(CustomerTable.pin_code == search_text)
    elif search_by == 'date_of_completion':
        query = query.filter(BaseTable.date_of_completion == search_text)
    
    
    
    results = query.add_columns(
        BaseTable.id,
        CustomerTable.full_name.label('customer_name'),
        CustomerTable.address,
        CustomerTable.pin_code,
        BaseTable.date_of_completion,
        BaseTable.service_rating.label('rating')
    ).all()
    
    response = []
    
    for result in results:
        print(result)
        response.append({
            'id': result.id,
            'customer_name': result.customer_name,
            'address': result.address,
            'pincode': result.pin_code,
            'date_of_completion': str(result.date_of_completion),
            'rating': result.rating
        })

    return jsonify(response), 200

#   Graph Data For Admin
@app.route('/api/admin_summary', methods=['GET'])
def admin_summary():
    print("Hello")
    # Querying the number of requests per service status (Closed, Requested, Accepted)
    service_status_counts = db.session.query(BaseTable.service_status, db.func.count(BaseTable.id)) \
        .group_by(BaseTable.service_status).all()

    status_mapping = {
        0: "Closed",
        1: "Requested",
        2: "Accepted"
    }

    # Preparing the service status data
    service_status_summary = {
        "Closed": 0,
        "Requested": 0,
        "Accepted": 0
    }

    for status, count in service_status_counts:
        service_status_summary[status_mapping.get(status, "Unknown")] = count

    # Query to get the count of each customer rating value
    ratings_count = db.session.query(BaseTable.service_rating, db.func.count(BaseTable.service_rating)) \
        .group_by(BaseTable.service_rating).all()

    # Preparing the customer ratings data
    rating_summary = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    }
    
    for rating, count in ratings_count:
        rating_summary[str(rating)] = count

    # Combining both results into a single response
    combined_summary = {
        "service_status_summary": service_status_summary,
        "rating_summary": rating_summary
    }
    print(combined_summary)
    
    return jsonify(combined_summary)

#   Admin Viewing Service Details Of All Users
@app.route('/api/search_service_summary', methods=['GET'])
def search_service_summary():
    category = request.args.get('category')
    search_text = request.args.get('text', '').lower()

    # Adjusting the query to ensure correct joins
    query = db.session.query(BaseTable, CustomerTable, ProfessionalTable).join(CustomerTable, BaseTable.customer_id == CustomerTable.customer_id) \
        .join(ProfessionalTable, BaseTable.professional_id == ProfessionalTable.professional_id)

    if category == 'service_name':
        query = query.join(ServiceTable, BaseTable.service_id == ServiceTable.id).filter(ServiceTable.name.ilike(f"%{search_text}%"))
    elif category == 'customer_name':
        query = query.filter(CustomerTable.full_name.ilike(f"%{search_text}%"))
    elif category == 'professional_name':
        query = query.filter(ProfessionalTable.full_name.ilike(f"%{search_text}%"))
    elif category == 'status':
        status_mapping = {
            'closed': 0,
            'requested': 1,
            'accepted': 2
        }
        status_value = status_mapping.get(search_text, None)
        if status_value is not None:
            query = query.filter(BaseTable.service_status == status_value)
        else:
            query = query.filter(BaseTable.service_status.isnot(None))
    else:
        query = query.filter(BaseTable.id.isnot(None))  # Default to not filtering if no valid category is given

    # Execute the query and fetch the results
    results = query.all()

    # Prepare the response data with the requested columns
    service_summary = []
    for service in results:
        service_data = {
            'Service ID': service[0].id,
            'Professional Assigned': service[2].full_name if service[2].full_name else "N/A",
            'Date Requested': service[0].date_of_request.strftime('%Y-%m-%d') if service[0].date_of_request else "N/A",
            'Customer Name': service[1].full_name if service[1].full_name else "N/A",
            'Status': "Closed" if service[0].service_status == 0 else "Requested" if service[0].service_status == 1 else "Accepted"
        }
        service_summary.append(service_data)

    return jsonify(service_summary)

#   Admin To Search Customers And Professionals
@app.route('/api/search_users', methods=['GET'])
def search_users():
    category = request.args.get('category')  # 'professional' or 'customer'
    search_text = request.args.get('text', '').strip()  # The search text

    if category == 'professional':
        # Query for professionals
        results = ProfessionalTable.query.filter(
            ProfessionalTable.full_name.ilike(f'%{search_text}%'),  # Search by name
            ProfessionalTable.approve == 1                         # Only approved professionals
        ).all()

        # Prepare response
        users = [
            {
                'id': professional.professional_id,
                'name': professional.full_name,
                'rating': professional.rating,
                'block': professional.block
            }
            for professional in results
        ]

    elif category == 'customer':
        # Query for customers
        results = CustomerTable.query.filter(
            CustomerTable.full_name.ilike(f'%{search_text}%')  # Search by name
        ).all()

        # Prepare response
        users = [
            {
                'id': customer.customer_id,
                'name': customer.full_name,
                'rating': None,  # Customers don't have a rating
                'block': customer.block
            }
            for customer in results
        ]
    else:
        return jsonify({'error': 'Invalid category'}), 400

    return jsonify(users)

#   Admin Able To Block Customers And Professionals
@app.route('/api/toggle_block', methods=['POST'])
def toggle_block():
    data = request.get_json()
    user_id = data.get('id')  # ID of the user
    category = data.get('category')  # 'professional' or 'customer'
    new_block_status = data.get('block')  # New block status (0 or 1)

    if category == 'professional':
        # Update professional block status
        professional = ProfessionalTable.query.get(user_id)
        if not professional:
            return jsonify({'error': 'Professional not found'}), 404
        professional.block = new_block_status
        db.session.commit()

    elif category == 'customer':
        # Update customer block status
        customer = CustomerTable.query.get(user_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        customer.block = new_block_status
        db.session.commit()

    else:
        return jsonify({'error': 'Invalid category'}), 400

    return jsonify({'success': True})


#------------------------------------------------- API Routes -----------------------------------------------------------------------------

api.add_resource(Professional_Service_Search_API, '/api/Professional_Service_Search')

api.add_resource(Customer_Summary_API, '/api/Customer_Summary')

api.add_resource(Professional_Summary_API, '/api/Professional_Summary')

api.add_resource(Professional_Today_Services_API, '/api/Professional_Today_Services')

api.add_resource(Professional_Closed_Services_API, '/api/Professional_Closed_Services')

api.add_resource(ServiceSummaryAPI, '/api/Service_Summary')

#------------------------------------------------- SQLite Tables -----------------------------------------------------------------------------

class BaseTable(db.Model):
    __tablename__ = 'Base_Table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('Service_Table.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer_Table.customer_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('Professional_Table.professional_id'), nullable=False)
    date_of_request = db.Column(db.Date, nullable=False)
    date_of_completion = db.Column(db.Date)
    service_status = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text)
    service_rating = db.Column(db.Integer)

    service = db.relationship('ServiceTable', backref='base_tables')
    customer = db.relationship('CustomerTable', backref='base_tables')
    professional = db.relationship('ProfessionalTable', backref='base_tables')

class CustomerTable(db.Model):
    __tablename__ = 'Customer_Table'
    
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    block = db.Column(db.Integer, default = 0)

class ProfessionalTable(db.Model):
    __tablename__ = 'Professional_Table'
    
    professional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.Text, nullable=False)
    service_name = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    document = db.Column(db.LargeBinary, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    approve = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer, default=5)
    block = db.Column(db.Integer, default = 0)

class ServiceTable(db.Model):
    __tablename__ = 'Service_Table'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    time_required = db.Column(db.Integer)

class AdminTable(db.Model):
    __tablename__ = 'Admin_Table'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

#------------------------------------------------- Role Selection Page -----------------------------------------------------------------------------

@app.route('/', methods = ["GET", "POST"])
def Role_Selection():
    if request.method == "GET":
        return render_template("Role_Selection.html")
    
    elif request.method == "POST":
        role = request.form.get('role')
        if role == 'admin':
            return redirect(url_for('Admin_Login'))
        elif role == 'customer':
            return redirect(url_for('Customer_SignUp'))
        elif role == 'professional':
            return redirect(url_for('Professional_SignUp'))
        else:
            return render_template("Error.html")
        
    else:
        return render_template("Error.html")

#------------------------------------------------- Login Pages -----------------------------------------------------------------------------

    
@app.route('/Customer_Login', methods = ["GET", "POST"]) 
def Customer_Login():
    if request.method == "GET":
        return render_template("Customer_Login.html")
    
    elif request.method == "POST":
        email_id = request.form.get('email_id')
        password = request.form.get('password')

        data = {
            'email_id': email_id,
            'password': password
        }

        response, status_code = Customer_Login_API().post(data)

        if status_code == 400 or status_code == 404 or status_code == 401:
            return render_template("Customer_Login.html", error = response.get('error'))
        
        elif status_code == 200:
            session['customer_id'] = response.get('customer_id')
            return redirect(url_for('Customer_Home_Page'))
        
        else:
            return render_template("Error.html", error = "Unknown Error???")
    
    else:
        return render_template("Error.html")
        

@app.route('/Admin_Login', methods = ["GET", "POST"])
def Admin_Login():
    if request.method == "GET":
        return render_template("Admin_Login.html")
    
    elif request.method == "POST":
        email_id = request.form.get('email_id')
        password = request.form.get('password')

        data = {
            'email_id': email_id,
            'password': password
        }

        response, status_code = Admin_Login_API().post(data)

        if status_code == 400 or status_code == 404 or status_code == 401:
            return render_template("Admin_Login.html", error = response.get('error'))
        
        elif status_code == 200:
            session['admin_id'] = response.get('admin_id')
            return redirect(url_for('Admin_Home_Page'))
        
        else:
            return render_template("Error.html", error = "Unknown Error???")
    
    else:
        return render_template("Error.html")


@app.route('/Professional_Login', methods = ["GET", "POST"])
def Professional_Login():
    if request.method == "GET":
        return render_template("Professional_Login.html")
    
    elif request.method == "POST":
        email_id = request.form.get('email_id')
        password = request.form.get('password')

        data = {
            'email_id': email_id,
            'password': password
        }

        response, status_code = Professional_Login_API().post(data)

        if status_code == 400 or status_code == 404 or status_code == 401:
            return render_template("Professional_Login.html", error = response.get('error'))
        
        elif status_code == 200:
            session['professional_id'] = response.get('professional_id')
            return redirect(url_for('Professional_Home_Page'))
        
        else:
            return render_template("Error.html", error = "Unknown Error???")
    
    else:
        return render_template("Error.html")

#------------------------------------------------- SignUp Pages -----------------------------------------------------------------------------

    
@app.route('/Customer_SignUp', methods = ["GET", "POST"])
def Customer_SignUp():
    if request.method == "GET":
        return render_template("Customer_SignUp.html")
    
    elif request.method == "POST":
        data = {
            'email_id': request.form.get('email_id'),
            'password': request.form.get('password'),
            'full_name': request.form.get('full_name'),
            'address': request.form.get('address'),
            'pincode': request.form.get('pincode')
        }

        response, status_code = Customer_Registration_API().post(data)

        if status_code == 200:
            return redirect(url_for('Customer_Login'))
        
        elif status_code == 400:
            return render_template('Customer_SignUp.html', error = response.get('error'))
        
        else:
            return render_template("Error.html", error = response.get('error', 'Unknown error'))
    
    else:
        return render_template("Error.html")
    
    
@app.route('/Professional_SignUp', methods = ["GET", "POST"])
def Professional_SignUp():
    if request.method == "GET":
        services = ServiceTable.query.all()
        return render_template("Professional_SignUp.html", services=services)
    
    elif request.method == "POST":
        doc_file = request.files['document']
        doc_file = doc_file.read()

        data = {
            'email_id': request.form.get('email_id'),
            'password': request.form.get('password'),
            'full_name': request.form.get('full_name'),
            'address': request.form.get('address'),
            'pincode': request.form.get('pincode'),
            'service_name': request.form.get('service_name'),
            'experience': request.form.get('experience'),
            'document': doc_file,  # Store binary PDF data
            'description': request.form.get('description')
        }

        response, status_code = Professional_API().post(data)

        if status_code == 200:
            return redirect(url_for('Professional_Login'))
        
        elif status_code == 400:
            return render_template('Professional_SignUp.html', error = response.get('error'))
        
        else:
            return render_template("Error.html", error = response.get('error', 'Unknown error'))
    
    else:
        return render_template("Error.html")
    
#------------------------------------------------- Home Pages -----------------------------------------------------------------------------

@app.route('/Customer_Home_Page', methods = ["GET", "POST"])
def Customer_Home_Page():
    if request.method == "GET":
        customer_id = session.get('customer_id')
        response, status_code = Check_Block_Customer_API().get()
        if response.get('is_blocked'):
            return render_template("Block_Page.html")
        else:
            return render_template("Customer_Home_Page.html", customer_id = customer_id)
    
    else:
        return render_template("Error.html", error = "Unknown Error")
    
@app.route('/Professional_Home_Page', methods = ["GET", "POST"])
def Professional_Home_Page():
    if request.method == "GET":
        professional_id = session.get('professional_id')
        response, status_code = Check_Block_Professional_API().get()
        if response.get('is_blocked'):
            return render_template("Block_Page.html")
        else:
            return render_template("Professional_Home_Page.html", professional_id = professional_id)
    
@app.route('/Admin_Home_Page', methods = ["GET", "POST"])
def Admin_Home_Page():
    if request.method == "GET":
        admin_id = session.get('admin_id')
        response, status_code = Services_API().get()
        response2, status_code2 = Professional_API().get()

        if status_code == 200 and status_code2 == 200:
            return render_template("Admin_Home_Page.html", services = response.get('services'), professionals = response2.get('professional_list'))
        else:
            return render_template("Error.html", error = response.get('error') + response2.get('error'))
    
#------------------------------------------------- Professional Profile Pages -----------------------------------------------------------------------------

@app.route('/Professional_Profile', methods = ["GET"])
def Professional_Profile():
    if request.method == "GET":
        professional_id = session.get('professional_id')
        response, status_code = Professional_Profile_API().get(professional_id)

        if status_code == 200:
            return render_template("Professional_Profile.html", professional = response)
        else:
            return render_template("Error.html", error=response.get('error'))
    
    else:
        return render_template("Error.html", error = "Unknown Error")

@app.route('/Professional_Edit_Profile', methods = ["GET", "POST"])
def Professional_Edit_Profile():
    if request.method == "GET":
        professional_id = session.get('professional_id')
        response, status_code = Professional_Profile_API().get(professional_id)

        if status_code == 200:
            return render_template("Professional_Edit_Profile.html", professional = response)
        else:
            return render_template("Error.html", error = response.get('error'))
        
    elif request.method == "POST":
        professional_id = session.get('professional_id')
        data = {
            'professional_id': professional_id,
            'full_name': request.form.get('full_name'),
            'address': request.form.get('address'),
            'pin_code': request.form.get('pin_code'),
            'description': request.form.get('description'),
            'experience': request.form.get('experience'),
        }

        response, status_code = Professional_Profile_API().put(data)

        if status_code == 200:
            return redirect(url_for('Professional_Profile'))
        else:
            return render_template("Error.html", error = response.get('error'))
        
    else:
        return render_template("Error.html", error = "Unknown Error")

#------------------------------------------------- Professional Summary -----------------------------------------------------------------------------

@app.route('/Professional_Summary', methods = ["GET"])
def Professional_Summary():
    if request.method == "GET":
        return render_template("Professional_Summary.html")

    else:
        return render_template("Error.html", error = "Unknown Error")
    
#------------------------------------------------- Admin Summary -----------------------------------------------------------------------------

@app.route('/Admin_Summary', methods = ["GET"])
def Admin_Summary():
    if request.method == "GET":
        return render_template("Admin_Summary.html")

    else:
        return render_template("Error.html", error = "Unknown Error")

#------------------------------------------------- Customer Profile Pages -----------------------------------------------------------------------------

@app.route('/Customer_Profile', methods = ["GET"])
def Customer_Profile():
    if request.method == "GET":
        customer_id = session.get('customer_id')
        response, status_code = Customer_Profile_API().get(customer_id)
        
        if status_code == 200:
            return render_template("Customer_Profile.html", customer = response)
        else:
            return render_template("Error.html", error=response.get('error'))
    
    else:
        return render_template("Error.html", error = "Unknown Error")
        

@app.route('/Customer_Edit_Profile', methods = ["GET", "POST"])
def Customer_Edit_Profile():
    if request.method == "GET":
        customer_id = session.get('customer_id')
        response, status_code = Customer_Profile_API().get(customer_id)

        if status_code == 200:
            return render_template("Customer_Edit_Profile.html", customer = response)
        else:
            return render_template("Error.html", error = response.get('error'))
        
    elif request.method == "POST":
        customer_id = session.get('customer_id')
        data = {
            'customer_id': customer_id,
            'full_name': request.form.get('full_name'),
            'address': request.form.get('address'),
            'pin_code': request.form.get('pin_code')
        }

        response, status_code = Customer_Profile_API().put(data)

        if status_code == 200:
            return redirect(url_for('Customer_Profile'))
        else:
            return render_template("Error.html", error = response.get('error'))
        
    else:
        return render_template("Error.html", error = "Unknown Error")

#------------------------------------------------- Customer Search -----------------------------------------------------------------------------

@app.route('/Customer_Search', methods = ["GET"])
def Customer_Search():
    if request.method == "GET":
        return render_template("Customer_Search.html")

    else:
        return render_template("Error.html", error = "Unknown Error")

#------------------------------------------------- Professional Search -----------------------------------------------------------------------------

@app.route('/Professional_Search', methods = ["GET"])
def Professional_Search():
    if request.method == "GET":
        return render_template("Professional_Search.html")

    else:
        return render_template("Error.html", error = "Unknown Error")

#------------------------------------------------- Admin Search -----------------------------------------------------------------------------

@app.route('/Admin_Search', methods = ["GET"])
def Admin_Search():
    if request.method == "GET":
        return render_template("Admin_Search.html")

    else:
        return render_template("Error.html", error = "Unknown Error")
        
#------------------------------------------------- Customer Summary -----------------------------------------------------------------------------

@app.route('/Customer_Summary', methods = ["GET"])
def Customer_Summary():
    if request.method == "GET":
        return render_template("Customer_Summary.html")

    else:
        return render_template("Error.html", error = "Unknown Error")

#------------------------------------------------- Customer Review / Closing Service -----------------------------------------------------------------------------

@app.route('/Close_Service/<int:service_id>', methods=['GET','POST'])
def Close_Service(service_id):
    if request.method == "GET":
        return render_template('Close_Service.html', service_id = service_id)
    
    elif request.method == "POST":
        data = {
            'service_id': service_id,
            'remarks': request.form.get('remarks'),
            'rating': float(request.form.get('rating'))
        }
        response, status_code = Close_Service_API().put(data)


        if status_code == 200:
            return redirect(url_for('Customer_Home_Page'))
        
        else:
            return jsonify({ "error": "No Such Service Available"})

    else:
        return render_template("Error.html", error = "Unknown Error")

#------------------------------------------------- Professional Accept / Reject -----------------------------------------------------------------------------

@app.route('/accept/<int:id>', methods = ["GET"])
def Accept(id):
    data = {
        'id': id,
        'case': 1
    }

    response, status_code = Professional_Accept_Reject_API().put(data)

    if status_code == 200:
        return redirect(url_for('Professional_Home_Page'))
    
    else:
        return render_template('Error.html', error = response.get('error'))
    
@app.route('/reject/<int:id>', methods = ["GET"])
def Reject(id):
    data = {
        'id': id,
        'case': 0
    }

    response, status_code = Professional_Accept_Reject_API().put(data)

    if status_code == 200:
        return redirect(url_for('Professional_Home_Page'))
    
    else:
        return render_template('Error.html', error = response.get('error'))

#------------------------------------------------- Admin Service Changes -----------------------------------------------------------------------------

@app.route('/Add_Service', methods = ["GET", "POST"])
def Add_Service():
    if request.method == "GET":
        return render_template('Add_Service.html')
    
    elif request.method == "POST":
        data = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': request.form.get('price'),
            'time_required': request.form.get('time_required')
        }

        response, status_code = Services_API().post(data)

        if status_code == 200:
            return redirect(url_for('Admin_Home_Page'))
        
        else:
            return render_template("Error.html", error = response.get('response'))
    
    else:
        return render_template("Error.html", error = "Unknown Error")
    
@app.route('/Edit_Service/<int:id>', methods=['GET', 'POST'])
def Edit_Service(id):
    if request.method == "GET":
        service = ServiceTable.query.get(id)
        return render_template('Edit_Service.html', service = service)
    
    elif request.method == 'POST':
        data = {
            'id': id,
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': request.form.get('price'),
            'time_required': request.form.get('time_required')
        }

        response, status_code = Services_API().put(data)

        if status_code == 200:
            return redirect(url_for('Admin_Home_Page'))
        
        else:
            return render_template("Error.html", error = response.get('error'))

    else:
        return render_template("Error.html", error = "Unknown Error")
    
@app.route('/Delete_Service/<int:id>', methods=['POST'])
def Delete_Service(id):
    if request.method == "POST":
        data = {
            'id': id
        }
        response, status_code = Services_API().delete(data)
        
        if status_code == 200:
            return redirect(url_for('Admin_Home_Page'))
        
        else:
            return render_template('Error.html', error = response.get('error'))
    
    else:
        return render_template("Error.html", error = "Unknown Error")
        

#------------------------------------------------- Admin Professional Changes -----------------------------------------------------------------------------

@app.route('/Approve_Professional/<int:id>', methods=['POST'])
def Approve_Professional(id):
    if request.method == "POST":
        data = {
            'professional_id': id,
            'case': 1
        }
        response, status_code = Professional_API().put(data)
        
        if status_code == 200:
            return redirect(url_for('Admin_Home_Page'))
        else:
            return render_template('Error.html', error = response.get('error'))
    else:
        return render_template("Error.html", error = 'Unknown Error')

@app.route('/Reject_Professional/<int:id>', methods=['POST'])
def Reject_Professional(id):
    if request.method == "POST":
        data = {
            'professional_id': id,
            'case': 0
        }
        response, status_code = Professional_API().put(data)
        
        if status_code == 200:
            return redirect(url_for('Admin_Home_Page'))
        else:
            return render_template('Error.html', error = response.get('error'))
    else:
        return render_template("Error.html", error = 'Unknown Error')

@app.route('/Delete_Professional/<int:id>', methods=['POST'])
def Delete_Professional(id):
    if request.method == "POST":
        response, status_code = Professional_API.delete(id)

        if status_code == 200:
            return redirect(url_for('admin_home'))
        else:
            return render_template("Error.html", error = response.get('error'))
    else:
        return render_template("Error.html", error = "Unknown Error")
    
#------------------------------------------------- PDF Files -----------------------------------------------------------------------------

@app.route('/Download_Document/<int:professional_id>', methods=['GET'])
def Download_Document(professional_id):
    professional = ProfessionalTable.query.get(professional_id)
    
    if professional and professional.document:
        return send_file(io.BytesIO(professional.document), download_name='document.pdf', as_attachment=True)
    else:
        abort(404)

#------------------------------------------------- Logout Page -----------------------------------------------------------------------------

@app.route('/Logout')
def Logout():
    session.clear()
    return render_template("Logout.html")

#------------------------------------------------- End -----------------------------------------------------------------------------
    
if __name__ == '__main__':
    app.run(debug = True, port = 8080)