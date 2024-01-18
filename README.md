 ## Table of Contents
1. [Introduction](#introduction)
2. [Key Features](#key-features)
    1. [Course Management](#course-management)
    2. [Module Creation](#module-creation)
    3. [Student Management](#student-management)
    4. [User Authentication](#user-authentication)
3. [Sample](#sample)
4. [Dependencies](#dependencies)
5. [Views](#views)
    1. [Index View](#index-view)
    2. [Classes View](#classes-view)
    3. [Register View](#register-view)
    4. [Login View](#login-view)
    5. [Logout View](#logout-view)
    6. [Check Login Status View](#check-login-status-view)
    7. [New Class View](#new-class-view)
    8. [View Class View](#view-class-view)
    9. [View Module View](#view-module-view)
    10. [Add Module View](#add-module-view)
    11. [Add Student View](#add-student-view)
    12. [Student Form View](#student-form-view)

## Introduction
Welcome to ClassroomBridge, a comprehensive Learning Management System (LMS) meticulously crafted for K-12 classrooms. This Django-powered app is a dynamic platform that empowers educators, students, and administrators by seamlessly integrating essential features to enhance the teaching and learning experience.

## Key Features

### Course Management
ClassroomBridge simplifies the organization of courses, allowing teachers to create, customize, and manage their class offerings. From academic subjects to extracurricular activities, this LMS provides a centralized hub for all educational endeavors.

### Module Creation
Enrich your curriculum with detailed modules. ClassroomBridge supports the creation of content-rich modules, providing educators with a versatile tool to structure lessons, share resources, and engage students effectively.

### Student Management
Effortlessly manage student enrollment and participation within classes. Teachers can keep track of student progress, assess performance, and foster a collaborative learning environment.

### User Authentication
Ensuring a secure and personalized experience, ClassroomBridge incorporates robust user authentication mechanisms. Teachers, students, and administrators can access designated views based on their roles, safeguarding sensitive information.

## Sample

![ClassroomBridge Example](ClassroomBridge/Bridge-Example1.png)
![ClassroomBridge Example](ClassroomBridge/Ms._Smith_Home.png)
---

## Dependencies
- Django
- Markdown2

## Views

### Index View
The `index` view renders the main landing page.

### Classes View
The `classes` view displays the classes associated with the logged-in user.

### Register View
The `register_view` handles user registration. It checks for matching passwords and ensures the uniqueness of email addresses.

### Login View
The `login_view` handles user login. It authenticates the user and redirects to the classes page upon successful login.

### Logout View
The `logout_view` logs out the current user and redirects to the index page.

### Check Login Status View
The `check_login_status` view returns a JSON response indicating whether the user is authenticated.

### New Class View
The `new_class` view handles the creation of a new class. It validates input and redirects to the classes page.

### View Class View
The `view_class` view displays details about a specific class, including its modules.

### View Module View
The `view_module` view displays details about a specific module within a class, converting markdown content to HTML for better rendering.

### Add Module View
The `add_module` view allows the addition of a new module to a class.

### Add Student View
The `add_student` view allows the addition of a new student to a class.

### Student Form View
The `student_form` view renders a form for adding a new student to a class.