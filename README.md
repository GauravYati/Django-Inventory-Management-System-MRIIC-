# MRIIC Research Lab Inventory Management System

A Django-based inventory management system built for the Manav Rachna Incubation and Innovation Center research lab. The project helps students discover available lab resources and lets authorized staff manage equipment records, stock quantities, featured resources, and borrow requests.

## Project Intention

Research labs often manage electronics, fabrication tools, safety items, sensors, and shared equipment through scattered spreadsheets or manual communication. This project was created to make that workflow clearer and more reliable:

- Students can browse lab resources before requesting them.
- Staff can maintain a centralized inventory.
- Borrow requests are reviewed before stock is deducted.
- Returned items can be marked by staff so stock is restored.
- The interface is designed for a research lab, not an online store.

## Features

- Modern student-facing inventory catalogue
- Search and category-based browsing
- Product/resource detail page
- Borrow request form for students
- Staff-only login flow
- Staff dashboard with inventory statistics
- Add, edit, update quantity, feature, and delete resources
- Borrow request approval, rejection, and return workflow
- Django admin customization for backend management
- Responsive UI for desktop and smaller screens

## Screenshots

Add your screenshots inside a folder like:

```text
docs/screenshots/
```

Then replace the placeholder paths below.

### Student View

#### Home Page

![Student Home Page](docs/screenshots/student-home.png)

#### Inventory Catalogue

![Student Inventory Catalogue](docs/screenshots/student-inventory.png)

#### Search Results

![Student Search Results](docs/screenshots/student-search.png)

#### Resource Detail and Borrow Request

![Student Resource Detail](docs/screenshots/student-resource-detail.png)

### Staff/Admin View

#### Staff Login

![Staff Login](docs/screenshots/staff-login.png)

#### Staff Dashboard

![Staff Dashboard](docs/screenshots/staff-dashboard.png)

#### Add Resource Form

![Add Resource Form](docs/screenshots/add-resource.png)

#### Edit Resource Form

![Edit Resource Form](docs/screenshots/edit-resource.png)

#### Django Admin Panel

![Django Admin Panel](docs/screenshots/django-admin.png)

## Tech Stack

- Python
- Django
- SQLite
- Bootstrap
- Bootstrap Icons
- django-taggit
- Pillow

## How The Project Works

The application has two main user flows.

### Student Flow

Students can open the inventory catalogue, search for resources, view item details, and submit a borrow request. A borrow request does not immediately reduce the available quantity. It first goes to staff for review.

### Staff Flow

Staff users sign in through the staff login page. From the dashboard, they can add new resources, edit existing resources, update quantities, mark resources as featured, delete records, and process borrow requests.

When staff approves a borrow request, the requested quantity is deducted from the item stock. When the item is returned, staff can mark it as returned, and the quantity is added back.

## Setup Instructions

You do not need Django installed globally. Install all dependencies inside a virtual environment.

### 1. Open The Project

```powershell
cd Django-Inventory-Management-System-MRIIC--Prototype-Branch
cd Django-Inventory-Management-System-MRIIC--Prototype-Branch
cd inventoryProject
```

### 2. Create A Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate The Virtual Environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Command Prompt:

```bat
.venv\Scripts\activate.bat
```

If activation is blocked in PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then close and reopen PowerShell and activate the environment again.

### 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r ..\requirements.txt
```

### 5. Apply Database Migrations

```powershell
python manage.py migrate
```

### 6. Create A Staff/Admin User

```powershell
python manage.py createsuperuser
```

Follow the prompts and remember the username and password. Use this account for the staff login and Django admin panel.

### 7. Run The Server

```powershell
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/
```

## Useful URLs

- Home: `http://127.0.0.1:8000/`
- Inventory catalogue: `http://127.0.0.1:8000/products/`
- Staff login: `http://127.0.0.1:8000/admin-login/`
- Staff dashboard: `http://127.0.0.1:8000/inventory/`
- Add resource: `http://127.0.0.1:8000/add-inventory/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Folder Structure

```text
inventoryProject/
|-- inventoryProject/      # Django project settings and URLs
|-- mriic/                 # Main inventory app
|   |-- migrations/        # Database migrations
|   |-- static/mriic/      # CSS and image assets
|   |-- templates/mriic/   # HTML templates
|   |-- admin.py           # Django admin configuration
|   |-- forms.py           # Django forms
|   |-- models.py          # Database models
|   `-- views.py           # App logic and page views
|-- media/                 # Uploaded item images
|-- db.sqlite3             # Local SQLite database
`-- manage.py              # Django command runner
```

## Database Models

- `Category`: Stores resource categories such as electronics, safety, fabrication, and measurement.
- `Item`: Stores inventory resources with image, quantity, description, categories, tags, and featured status.
- `BorrowRequest`: Stores student borrow requests and tracks pending, approved, returned, and rejected states.

## Borrow Request Logic

1. Student submits a borrow request from a resource detail page.
2. Staff receives the request in the staff dashboard.
3. Staff can approve or reject the request.
4. Approval deducts the requested quantity from stock.
5. When the resource is returned, staff marks it as returned.
6. Return status adds the quantity back to stock.

## Authentication

The management area is restricted to staff users. Regular visitors can browse and submit borrow requests, but only staff/admin accounts can add, edit, delete, approve, reject, or return inventory records.

### Demo Staff Login

```text
Username: Gaurav
Password: 1234
```

Use this account from the staff login page if it exists in your local database. If it does not work after setting up the project, create a new staff/admin account with:

```powershell
python manage.py createsuperuser
```

## Testing Plan

Playwright end-to-end tests will be added for the main student and staff workflows, including inventory browsing, search, staff login, resource creation/editing, and borrow request approval/return flow.

## Author

Created by **Gaurav Yati**.

This project originally started as a college-time team prototype for MRIIC. It was left partially unfinished at that stage, so I later revisited it to improve the UI, clean the workflow, make the inventory experience more polished, and turn it into a more complete research lab management system.
