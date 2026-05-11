# KBS Bakery 

## Project Overview

KBS Bakery is a Flask-based web application developed for managing online bakery orders. The system allows users to browse cakes and Indian sweets, add products to cart, update quantities and weights, proceed to checkout, and place orders through a simulated payment system.

The project demonstrates full-stack web development concepts including backend programming, frontend design, database integration, session management, and inventory handling using Python Flask and SQLite.

---

# Objectives

- Develop a bakery ordering web application
- Implement database connectivity using SQLite
- Manage user sessions and cart functionality
- Demonstrate CRUD operations
- Simulate checkout and payment workflow
- Apply frontend and backend integration concepts

---

# Features

## User Features
- User Login System
- Browse Cakes and Indian Sweets
- Add Items to Cart
- Update Cart Quantity and Weight
- Remove Products from Cart
- Checkout System
- Payment Method Selection
- Order Confirmation Page

## Admin/System Features
- SQLite Database Integration
- Product Inventory Management
- Stock Availability Checking
- Automatic Stock Reduction After Order
- Session Handling
- Dynamic Total Price Calculation

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Programming |
| Flask | Web Framework |
| SQLite | Database |
| HTML | Frontend Structure |
| CSS | Frontend Styling |
| Jinja2 | Dynamic Templates |

---

# Database Tables

## Products Table
Stores:
- Product Name
- Price
- Stock Availability

## Orders Table
Stores:
- Customer Name
- Address
- Phone Number
- Payment Method
- Total Amount

## Order Items Table
Stores:
- Ordered Product Details
- Quantity
- Weight
- Subtotal

---

# Python Concepts Used

- Functions
- Flask Routing
- Session Handling
- Lists and Dictionaries
- Conditional Statements
- Loops
- CRUD Operations
- Database Connectivity
- Form Handling
- Dynamic Rendering using Jinja2

---

# Flask Features Used

- Flask Routing
- HTML Template Rendering
- POST and GET Methods
- Session Management
- Redirect Handling

---

# How the System Works

1. User logs into the system
2. User browses cakes and sweets
3. User selects weight and quantity
4. Product is added to cart
5. User updates or removes cart items
6. User proceeds to checkout
7. User selects payment method
8. Order details are stored in SQLite database
9. Stock quantity gets updated automatically
10. Order confirmation page is displayed

---

# How to Run the Project

## Step 1
Install dependencies:

```bash
pip install -r requirements.txt
```

## Step 2
Run Flask application:

```bash
python app.py
```

## Step 3
Open browser:

```text
http://127.0.0.1:5000
```

---

# Login Credentials

```text
Username: admin
Password: 1234
```

---

# Project Structure

```text
KBS BAKERY/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── cakes.html
│   ├── cart.html
│   ├── checkout.html
│   ├── payment.html
│   └── success.html
│
├── static/
│   └── style.css
```

---

# Future Enhancements

- Admin Dashboard
- User Registration System
- Order Tracking
- Email Notifications
- Responsive Mobile Design

---

# Team Members

- Kavya Veeramreddy
- Bala Bhavya Bhimineni
- Shanker Utkur

---

# Academic Purpose

This project was developed for academic learning purposes to understand Flask web development, SQLite database integration, frontend-backend communication, and web application architecture.

---

# Conclusion

KBS Bakery successfully demonstrates the implementation of a dynamic bakery ordering system using Flask and SQLite. The project integrates frontend and backend technologies to provide a complete user ordering experience while maintaining product inventory and order management functionality.
