from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseTable(db.Model):
    """
    Represents a service booking between a customer and a professional.
    Tracks status, dates, and ratings for each service instance.
    """
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
    """
    Stores customer account and profile information.
    Used for authentication and service booking.
    """
    __tablename__ = 'Customer_Table'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    block = db.Column(db.Integer, default = 0)


class ProfessionalTable(db.Model):
    """
    Stores professional account, profile, and service details.
    Used for authentication, approval, and service assignment.
    """
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
    """
    Represents a type of service offered on the platform.
    Linked to professionals and bookings.
    """
    __tablename__ = 'Service_Table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    time_required = db.Column(db.Integer)


class AdminTable(db.Model):
    """
    Stores admin account credentials for platform management.
    """
    __tablename__ = 'Admin_Table'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
