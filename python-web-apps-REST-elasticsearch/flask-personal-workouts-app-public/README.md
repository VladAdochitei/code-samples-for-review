# flask-personal-workouts-app
This application also was done as part of one subject I had at my Master's degree, it is a very simple API written in Python Flask that is connected to an ElasticSearch backend used for storing data that is published to the api. In a real scenario we would use a Relational or Document Database system for this task but for that subject it was required to use ElasticSearch to better understand its features and interaction model.

----------------------
## Contents:
- [1. Overview](#1-overview)
- [2. Tech Stack](#2-tech-stack)
- [3. Models](#3-models)
- [4. REST API Structure](#4-rest-api-structure)
----------------------


## 1. Overview
My workout tracker application aims to streamline my outdoor exercise routines by offering a comprehensive platform to **record**, **manage**, and **visualize** various workout activities. The application is primarily designed to focus on outdoor workouts, including *running*, *climbing*, *swimming*, *cycling*, and *calisthenics*. The main functionalities of the application are:
- Login/Register:
    - Ability to log in and log out from the application, also the ability to register a new account.
    - The authentication mechanism will allow to render only the workouts of the user that's currently authenticated.
- Record Workouts:
    - Log various workout types (running, climbing, swimming, cycling, calisthenics).
    - Capture details: date, duration, distance, location, notes/description.
- Manage Workouts:
    - View workout history.
    - Edit or delete recorded workouts.
- Map Integration (Leaflet):
    - Display workout locations.
    - Custom markers/icons for workout types.
    - Interactive details on map markers.
- Task Tracking (Optional Enhancements):
    - Track workout statistics (distance covered, average duration).

## 2. Tech stack
The application will be developed using the following technologies:

- Backend (**Flask** - Python): 
    - the backend will be developed using the python's ***flask*** framework
- Database (**SQLite** - SQL):
    - The database that will be used is SQLite (In Memory database). It is a simple and very lightweight database, suitable for web applications that are planned to have little to medium transactions.
    - SQLAlchemy will be used as an ORM
- Frontend (**HTML**, **CSS**, **JS**, possibly **JQuery** + **Bootstrap**):
    - **HTML/CSS**: Form the structure and styling of your application.
    - **JavaScript**: Enables client-side interactivity and dynamic content rendering.
    - **jQuery**: Facilitates DOM manipulation and event handling, making interactions smoother.
    - **Bootstrap**: Offers a library of ready-to-use UI components, grids, and styles that enhance responsiveness and aesthetics without starting from scratch.
    - The **Leaflet** library will be used to render the map and different map-related elements, pins, coordinates, etc.
- ElasticSearch for searching through the workouts at a great speed.

## 3. Models
Considering we have an application focused around workouts and users, the first two models that should be added are: 
- User
- Workout 

Further describing the models will reveal:
- **User Model**:
    - *ID*: Unique identifier for each user.
    - *Username*: User's login identifier.
    - *Password*: Encrypted password for user authentication.

- **Workout Model**:
    - *ID*: Unique identifier for each workout.
    - *UserId*: Identifier linking the workout to a specific user.
    - *Type*: Type of workout (e.g., running, swimming, calisthenics).
    - *Date*: Date when the workout occurred.
    - *Duration*: Duration of the workout in minutes or hours.
    - *Distance*: Distance covered during the workout (optional).
    - *Location*: Location where the workout took place (optional).
    - *Notes*: Additional details or comments about the workout (optional).

## 4. REST API Structure
The structure for the REST API interface required by our application to function will be the following:

| HTTP Method | Route                         | Description (Users)                                    |
|-------------|-------------------------------|--------------------------------------------------------|
| GET         | /api/users                    | Get all users (for admin or future expansion)          |
| POST        | /api/users                    | Create a new user                                      |
| GET         | /api/users/{user_id}          | Get a specific user by ID, and its associated data     |
| PUT         | /api/users/{user_id}          | Update user details                                    |
| DELETE      | /api/users/{user_id}          | Delete a user                                          |

| HTTP Method | Route                         | Description (Workouts)                                 |
|-------------|-------------------------------|--------------------------------------------------------|
| GET         | /api/users/{user_id}/workouts | Get all workouts for a specific user                   |
| POST        | /api/users/{user_id}/workouts | Create a new workout for a specific user               |
| GET         | /api/users/{user_id}/workouts/{workout_id} | Get a specific workout for a user         |
| PUT         | /api/users/{user_id}/workouts/{workout_id} | Update a specific workout for a user      |
| DELETE      | /api/users/{user_id}/workouts/{workout_id} | Delete a specific workout for a user      |

These routes assume a RESTful API structure where `/api/users` handles user-related operations and `/api/users/{user_id}/workouts` manages workout-related endpoints for specific users. Adjustments or additional routes might be necessary based on your application's specific requirements and functionalities.

## 5. Elastic context

### 5.1. Index

![index](./1-index-settings.png)

### 5.2. Index Mapping


![mapping](./2-mappings.png)

Note:
Use CamelCase.
Add filter keyword to filter users on GET request.
Don't need UI, ElasticSearch will act as the UI.
Don't Need DB, ElasticSearch will act as Database.