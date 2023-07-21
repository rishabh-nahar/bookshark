# BookShark - Second Hand Book Selling and Buying Platform

BookShark is a web application developed using Django that facilitates the buying and selling of second-hand books, similar to the popular online platform OLX.com. The application provides a user-friendly interface for users to explore, list, and purchase used books.

## Features

- User Registration: Users can create an account by providing their essential details, including username, email, first name, middle name, last name, gender, and password.

- User Profile: Each user has a profile page that displays their personal information, including name, gender, contact number, and address.

- Book Listing: Users can list their second-hand books for sale. When listing a book, they need to provide book details, such as book name, category, author, publisher, year of edition, selling price, MRP, and a brief book description.

- Book Images: Sellers can upload images of the book they wish to sell, allowing potential buyers to view the book's condition.

- Book Search: Users can search for books based on their title, category, author, or any other relevant keywords.

- User Authentication: BookShark uses Django's authentication system to manage user login and logout.

- Email Notifications: The application sends email notifications using SMTP for account creation and other important updates.

## Getting Started

To set up BookShark on your local machine, follow these steps:

1. Clone or download the repository to your local machine.
2. Ensure you have Python and Django installed.
3. Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

Set up the database by running the migrations:
```bash
python manage.py migrate
```

Create a superuser account to access the Django admin panel:
```bash
python manage.py createsuperuser
```

Start the development server:
```bash
python manage.py runserver
```

Access the application by visiting http://localhost:8000 in your web browser.
```bash
http://localhost:8000 
```
