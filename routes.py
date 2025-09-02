from flask import render_template, request, redirect, url_for, jsonify, session, send_file, abort
from datetime import datetime
from sqlalchemy import not_
from models import db, CustomerTable, ProfessionalTable, AdminTable, ServiceTable, BaseTable
from api_resources import (
    Customer_Login_API, Admin_Login_API, Professional_Login_API, Customer_Registration_API, Professional_API, Services_API, 
    Customer_Profile_API, Professional_Profile_API, Close_Service_API, Check_Block_Customer_API, Check_Block_Professional_API, 
    Professional_Accept_Reject_API
)

# All Flask route/view functions from app.py are moved here. No logic is changed.
# This file is meant to be imported and registered in app.py


# --- Role Selection Page ---
def Role_Selection():
    """
    Render the role selection page and handle role-based redirection.
    """
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

# --- Login Pages ---
def Customer_Login():
    """
    Render the customer login page and handle login authentication.
    """
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

def Admin_Login():
    """
    Render the admin login page and handle login authentication.
    """
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

def Professional_Login():
    """
    Render the professional login page and handle login authentication.
    """
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


# --- SignUp Pages ---
def Customer_SignUp():
    """
    Render the customer signup page and handle registration.
    """
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

def Professional_SignUp():
    """
    Render the professional signup page and handle registration.
    """
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
            'document': doc_file,
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

# --- Home Pages ---
def Customer_Home_Page():
    """
    Render the customer home page and check block status.
    """
    if request.method == "GET":
        customer_id = session.get('customer_id')
        response, status_code = Check_Block_Customer_API().get()
        if response.get('is_blocked'):
            return render_template("Block_Page.html")
        else:
            return render_template("Customer_Home_Page.html", customer_id = customer_id)
    else:
        return render_template("Error.html", error = "Unknown Error")

def Professional_Home_Page():
    """
    Render the professional home page and check block status.
    """
    if request.method == "GET":
        professional_id = session.get('professional_id')
        response, status_code = Check_Block_Professional_API().get()
        if response.get('is_blocked'):
            return render_template("Block_Page.html")
        else:
            return render_template("Professional_Home_Page.html", professional_id = professional_id)

def Admin_Home_Page():
    """
    Render the admin home page with service and professional lists.
    """
    if request.method == "GET":
        admin_id = session.get('admin_id')
        response, status_code = Services_API().get()
        response2, status_code2 = Professional_API().get()
        if status_code == 200 and status_code2 == 200:
            return render_template("Admin_Home_Page.html", services = response.get('services'), professionals = response2.get('professional_list'))
        else:
            return render_template("Error.html", error = response.get('error') + response2.get('error'))

# --- Profile Pages ---
def Professional_Profile():
    """
    Render the professional profile page.
    """
    if request.method == "GET":
        professional_id = session.get('professional_id')
        response, status_code = Professional_Profile_API().get(professional_id)
        if status_code == 200:
            return render_template("Professional_Profile.html", professional = response)
        else:
            return render_template("Error.html", error=response.get('error'))
    else:
        return render_template("Error.html", error = "Unknown Error")

def Professional_Edit_Profile():
    """
    Render and handle editing of the professional profile.
    """
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

def Professional_Summary():
    """
    Render the professional summary page.
    """
    if request.method == "GET":
        return render_template("Professional_Summary.html")
    else:
        return render_template("Error.html", error = "Unknown Error")

def Admin_Summary():
    """
    Render the admin summary page.
    """
    if request.method == "GET":
        return render_template("Admin_Summary.html")
    else:
        return render_template("Error.html", error = "Unknown Error")

def Customer_Profile():
    """
    Render the customer profile page.
    """
    if request.method == "GET":
        customer_id = session.get('customer_id')
        response, status_code = Customer_Profile_API().get(customer_id)
        if status_code == 200:
            return render_template("Customer_Profile.html", customer = response)
        else:
            return render_template("Error.html", error=response.get('error'))
    else:
        return render_template("Error.html", error = "Unknown Error")

def Customer_Edit_Profile():
    """
    Render and handle editing of the customer profile.
    """
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

# --- Search Pages ---
def Customer_Search():
    """
    Render the customer search page.
    """
    if request.method == "GET":
        return render_template("Customer_Search.html")
    else:
        return render_template("Error.html", error = "Unknown Error")

def Professional_Search():
    """
    Render the professional search page.
    """
    if request.method == "GET":
        return render_template("Professional_Search.html")
    else:
        return render_template("Error.html", error = "Unknown Error")

def Admin_Search():
    """
    Render the admin search page.
    """
    if request.method == "GET":
        return render_template("Admin_Search.html")
    else:
        return render_template("Error.html", error = "Unknown Error")

def Customer_Summary():
    """
    Render the customer summary page.
    """
    if request.method == "GET":
        return render_template("Customer_Summary.html")
    else:
        return render_template("Error.html", error = "Unknown Error")

# --- Customer Review / Closing Service ---
def Close_Service(service_id):
    """
    Render and handle closing a service and submitting a review.
    """
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

# --- Professional Accept / Reject ---
def Accept(id):
    """
    Handle professional acceptance of a service request.
    """
    data = {
        'id': id,
        'case': 1
    }
    response, status_code = Professional_Accept_Reject_API().put(data)
    if status_code == 200:
        return redirect(url_for('Professional_Home_Page'))
    else:
        return render_template('Error.html', error = response.get('error'))

def Reject(id):
    """
    Handle professional rejection of a service request.
    """
    data = {
        'id': id,
        'case': 0
    }
    response, status_code = Professional_Accept_Reject_API().put(data)
    if status_code == 200:
        return redirect(url_for('Professional_Home_Page'))
    else:
        return render_template('Error.html', error = response.get('error'))

# --- Admin Service Changes ---
def Add_Service():
    """
    Render and handle adding a new service (admin only).
    """
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

def Edit_Service(id):
    """
    Render and handle editing a service (admin only).
    """
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

def Delete_Service(id):
    """
    Handle deleting a service (admin only).
    """
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

# --- Admin Professional Changes ---
def Approve_Professional(id):
    """
    Handle admin approval of a professional.
    """
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

def Reject_Professional(id):
    """
    Handle admin rejection of a professional.
    """
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

def Delete_Professional(id):
    """
    Handle admin deletion of a professional.
    """
    if request.method == "POST":
        response, status_code = Professional_API.delete(id)
        if status_code == 200:
            return redirect(url_for('admin_home'))
        else:
            return render_template("Error.html", error = response.get('error'))
    else:
        return render_template("Error.html", error = "Unknown Error")

# --- PDF Files ---
def Download_Document(professional_id):
    """
    Allow admin to download a professional's document (PDF).
    """
    professional = ProfessionalTable.query.get(professional_id)
    if professional and professional.document:
        return send_file(io.BytesIO(professional.document), download_name='document.pdf', as_attachment=True)
    else:
        abort(404)

# --- Logout Page ---
def Logout():
    """
    Log out the current user and clear the session.
    """
    session.clear()
    return render_template("Logout.html")

#   To Get All The Services Being Searched By Customer
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
def get_services():
    services = ServiceTable.query.all()
    return jsonify([{'name': service.name} for service in services])

#   To Get All Professionals Of A Particular Service
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
def admin_summary():
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
    
    return jsonify(combined_summary)

#   Admin Viewing Service Details Of All Users
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