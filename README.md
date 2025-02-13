Introduction:
The Household Services web application facilitates smooth interaction and exchange between 
customers and professionals, with an administrator overseeing the entire process. It supports seamless 
service requests created by customers, which are then processed by professionals. The project was 
designed to handle various tasks, such as service booking, customer and professional management, 
and data visualization.
This project uses the Flask framework for the backend, with Flask-SQLAlchemy to manage 
database interactions via SQLite. The frontend is developed using HTML and CSS for structure and 
styling, while Chart.js is used for interactive data visualization.
Admin Module:
The admin is initially directed to the Dashboard, which displays a list of services along with options 
to edit, delete, or create new services, allowing professionals to offer services in different fields.
There is also a list of professionals awaiting approval to provide services, which the admin can view 
and act upon.
The admin can view a summary list of services and all the details associated with them, including the 
customer name, professional name, service ID, and service status.
The Search function allows the admin to search for professionals or customers by name and provides 
the option to block/unblock users based on their ratings or negative feedback. This functionality 
helps the admin manage users and professionals efficiently.
The Summary function directs the admin to a page where the data related to services and customer 
ratings can be visualized in the form of graphs.
Customer Module:
The customer is directed to the Dashboard, where available services are displayed along with the 
professionals who offer them. This allows the customer to book services from professionals in specific 
fields.
The customer can also view their service request history and has the option to close any ongoing 
requests.
The Search function enables the customer to find professionals based on service name, pincode, and 
experience, and allows them to book services accordingly.
The Summary function presents a graph that visualizes the status of services related to the customer.
The Profile function enables the customer to view and edit their profile details.
Professional Module:
The professional is redirected to the Dashboard, where a list of service requests from customers 
(that have not yet been accepted or rejected) is shown. The professional can then choose to accept 
or reject these service requests.
The professional can also view all services they have completed, which includes service ID, customer 
name, address, pincode, date of completion, and service rating.
The Search function allows the professional to search for services by address, pincode, and date of 
completion, displaying a summary of services that match the search criteria.
The Summary function shows data regarding the status of the services handled by the professional, 
such as closed, requested, and assigned.
The Profile function allows the professional to view and edit their profile details.
