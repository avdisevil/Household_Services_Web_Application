Introduction

The Household Services web application is designed to facilitate seamless interaction and exchange between customers and professionals, with an administrator overseeing the entire process. It supports various tasks, including service booking, customer and professional management, and data visualization. The project is built using:

Backend: Flask framework
Database: Flask-SQLAlchemy with SQLite
Frontend: HTML and CSS
Data Visualization: Chart.js
The application aims to create a smooth and efficient platform for users to request and provide services, with detailed management features for both customers and professionals.

Admin Module
The Admin has access to a comprehensive dashboard with several management features:

Dashboard: Displays a list of available services with options to:

Edit
Delete
Create new services
Service Management: Admin can:

View a summary of all services, including customer names, professional names, service ID, and service status.
Act on professional approvals or rejections.
User Management:

View and manage professionals awaiting approval.
Search for professionals or customers by name.
Block or unblock users based on ratings or negative feedback.
Data Visualization:

The Summary function shows graphs related to services and customer ratings.
Provides an overview of performance metrics.
Customer Module
The Customer has access to a user-friendly dashboard to manage service requests:

Dashboard: Displays available services and professionals for easy booking.

Service History: Customers can:

View their service request history.
Close ongoing requests.
Search Function:

Search for professionals based on service name, pincode, and experience.
Book services according to search results.
Data Visualization:

The Summary function presents graphs visualizing the status of the customer’s services.
Profile Management:

Allows customers to view and edit their profile details.
Professional Module
The Professional dashboard helps manage service requests and completed tasks:

Dashboard: Displays a list of unassigned service requests that professionals can accept or reject.

Service Management:

View a history of completed services, including details such as service ID, customer name, address, pincode, date of completion, and service rating.
Search Function:

Professionals can search for services by address, pincode, or date of completion.
Data Visualization:

The Summary function provides data about the status of handled services (closed, requested, assigned).
Profile Management:

Allows professionals to view and edit their profile details.
