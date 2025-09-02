from flask_restful import Resource
from flask import jsonify, request, session
from datetime import datetime
from models import db, CustomerTable, ProfessionalTable, AdminTable, ServiceTable, BaseTable

class Customer_Registration_API(Resource):
    """
    API Resource for customer registration.
    Handles POST requests to register a new customer.
    """
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

class Customer_Login_API(Resource):
    """
    API Resource for customer login.
    Handles POST requests for customer authentication.
    """
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

class Professional_Login_API(Resource):
    """
    API Resource for professional login.
    Handles POST requests for professional authentication.
    """
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

class Admin_Login_API(Resource):
    """
    API Resource for admin login.
    Handles POST requests for admin authentication.
    """
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

class Customer_Profile_API(Resource):
    """
    API Resource for customer profile management.
    Handles GET and PUT requests for customer profile data.
    """
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

class Professional_Profile_API(Resource):
    """
    API Resource for professional profile management.
    Handles GET and PUT requests for professional profile data.
    """
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

class Services_API(Resource):
    """
    API Resource for CRUD operations on services.
    Handles GET, POST, PUT, DELETE requests for services.
    """
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

class Professional_API(Resource):
    """
    API Resource for professional management.
    Handles GET, POST, PUT, DELETE requests for professionals.
    """
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

class Close_Service_API(Resource):
    """
    API Resource for closing a service and updating ratings.
    Handles PUT requests to close a service.
    """
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

class Customer_Summary_API(Resource):
    """
    API Resource for customer service summary statistics.
    Handles GET requests for summary data.
    """
    def get(self):
        customer_id = session.get('customer_id')
        assigned = BaseTable.query.filter(BaseTable.service_status == 2, BaseTable.customer_id == customer_id).count()
        closed = BaseTable.query.filter(BaseTable.service_status == 0, BaseTable.customer_id == customer_id).count()
        requested = BaseTable.query.filter(BaseTable.service_status == 1, BaseTable.customer_id == customer_id).count()
        if customer_id:
            return {'assigned': assigned, 'closed': closed, 'requested': requested}, 200
        else:
            return {'error': 'No Customer Logged In'}, 401

class Professional_Summary_API(Resource):
    """
    API Resource for professional service summary statistics.
    Handles GET requests for summary data.
    """
    def get(self):
        professional_id = session.get('professional_id')
        assigned = BaseTable.query.filter(BaseTable.service_status == 2, BaseTable.professional_id == professional_id).count()
        closed = BaseTable.query.filter(BaseTable.service_status == 0, BaseTable.professional_id == professional_id).count()
        requested = BaseTable.query.filter(BaseTable.service_status == 1, BaseTable.professional_id == professional_id).count()
        if professional_id:
            return {'assigned': assigned, 'closed': closed, 'requested': requested}, 200
        else:
            return {'error': 'No Professional Logged In'}, 401

class Professional_Service_Search_API(Resource):
    """
    API Resource for searching closed services by professionals.
    Handles GET requests with search filters.
    """
    def get(self):
        search_by = request.args.get('by')
        search_text = request.args.get('text')
        professional_id = session.get('professional_id')
        if not professional_id:
            return {'error': 'No Professional Logged In'}, 401
        query = BaseTable.query.filter(BaseTable.service_status == 0, BaseTable.professional_id == professional_id)
        if search_by == 'address':
            query = query.filter(ProfessionalTable.address.ilike(f'%{search_text}%'))
        elif search_by == 'pincode':
            query = query.filter(ProfessionalTable.pin_code == search_text)
        elif search_by == 'date_of_completion':
            query = query.filter(BaseTable.date_of_completion == search_text)
        results = query.join(CustomerTable, BaseTable.customer_id == CustomerTable.customer_id).all()
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

class ServiceSummaryAPI(Resource):  
    """
    API Resource for admin to view a summary of all services.
    Handles GET requests for service summary data.
    """
    def get(self):
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

class Professional_Today_Services_API(Resource):
    """
    API Resource for professionals to view today's assigned services.
    Handles GET requests for today's services.
    """
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

class Professional_Closed_Services_API(Resource):
    """
    API Resource for professionals to view closed/completed services.
    Handles GET requests for closed services.
    """
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

class Professional_Accept_Reject_API(Resource):
    """
    API Resource for professionals to accept or reject service requests.
    Handles PUT requests for assignment actions.
    """
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

class Check_Block_Customer_API(Resource):
    """
    API Resource to check if a customer is blocked.
    Handles GET requests for block status.
    """
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

class Check_Block_Professional_API(Resource):
    """
    API Resource to check if a professional is blocked.
    Handles GET requests for block status.
    """
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

