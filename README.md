# Gustavo Jimenez T2A2
#### Web server API

### [my workout_webAPI project in git](https://github.com/Gus14939/workout_webAPI)

## Installation
In a terminal, run the following commands:

1. navigate to GustavoJimenez_T2A2 folder `cd` into src folder
2. python3 -m venv .venv
3. .venv/Scripts/activate (Windows) or source .venv/bin/activate (MacOS/Linux)
pip install -r requirements.txt
flask db create_tables && flask db seed_tables
flask run
Testing/Usage
Open Insomnia and import the <u>GustavoJimenez-Insomnia_Workout_webAPI.json</u> file to get all endpoints imported. This could also be opened as http://localhost:8888/ in Insomnia.


## Requirement

## R1	Identification of the problem you are trying to solve by building this particular app.

Maintaining a consistent fitness routine can be challenging due to lack of accountability and motivation. Without support or a clear plan, it's easy to stray from fitness goals. To combat this, finding a workout buddy, joining a class, or using a fitness app for reminders and tracking progress helps stay on track.

Tracking progress effectively is another hurdle. Implementing a structured system like a workout journal or fitness tracking apps can streamline this process and provide valuable insights.

The absence of structured workouts can hinder achieving desired outcomes. Seeking guidance from professionals, following tailored plans, or using workout apps for personalized routines can create effective programs for better results and overall fitness success.

Entering the fitness world can feel overwhelming, especially in structuring routines. Without guidance, both newcomers and experienced individuals can struggle with exercise choices, risking loss of interest and progress.

To address this, accessing structured workout plans tailored to specific needs and goals, whether through trainers or reputable websites, provides a framework for success. However, these resources can sometimes be costly or lack a user-friendly platform for trainers to create daily workouts.

## R2	Why is it a problem that needs solving?

Without a clear plan, individuals, especially beginners, will struggle to devise effective exercise regimens, often resulting in suboptimal results and setbacks. This lack of guidance not only hampers progress but also makes it difficult to track performance accurately, leading to diminished motivation and accountability.

The absence of structured workouts heightens the risk of injury as individuals may engage in activities without proper guidance on form and progression. This not only undermines fitness progress but also poses a significant barrier to sustained participation in physical activity. To mitigate these challenges, implementing structured workouts through a fitness app, tailored to by individual needs offers a viable solution. By providing clear direction, accountability, structured workouts optimise their efforts, leading to improved results and engagement.

## R3	Why have you chosen this database system? What are the drawbacks compared to others?

When comparing PostgreSQL, MySQL, and SQLite for a workout manager web app, PostgreSQL emerges as the optimal choice due to its comprehensive feature set, robustness, and scalability, particularly for managing structured data and enforcing data integrity constraints.

**PostgreSQL** is known for its advanced features and extensibility, excels in handling complex relational data models, making it an ideal fit for the workout manager's schema. Its support for advanced data types, such as `JSONB`, enables flexible storage and querying of workout routines, exercises, and user data. Additionally, PostgreSQL's **ACID** compliance ensures data integrity, critical for maintaining accurate and reliable workout records.

While **MySQL** offers performance advantages for read-heavy workloads and simpler data models, it lacks some of PostgreSQL's advanced features, such as full-text search and `JSONB` support. These features are invaluable for enhancing the functionality and usability of the workout manager app, allowing users to search for exercises, track progress, and personalise workout routines effectively.

**SQLite**, while lightweight and suitable for embedded systems or mobile apps with low data volumes, may not provide the scalability and concurrency capabilities required for an ideally, always growing workout manager web app. The lack of client-server architecture and limited support for concurrent connections make it less suitable for handling the potentially high transaction volumes and user interactions typical of a web-based fitness application.

In conclusion, **PostgreSQL** stands out as the best choice for the workout manager web app, offering a suitalbe feature set, robustness, and scalability necessary for managing structured workout data effectively. With advanced capabilities like, support for complex data types and data integrity enforcement, make it the ideal database system to reliably power a fitness management platform.

## R4	Identify and discuss the key functionalities and benefits of an ORM


- **What is an ORM?**
   - An ORM is a framework that bridges the gap between object-oriented programming (OOP) and relational databases. It simplifies the translation of objects and their relationships into relational database tables.
   - ORM tools use class definitions (models) to create, maintain, and provide full access to objects' data and their database persistence.

- **Advantages of Using an ORM:**
   - **Speeds Up Development Time**:
     - ORM tools streamline data access code, reducing the need for manual SQL queries.
     - Developers can focus on business logic rather than low-level database interactions.
   - **Cost-Effective**:
     - ORM reduces development effort, leading to cost savings.
     - Maintenance becomes easier due to consistent data access patterns.
   - **Handles Database Logic**:
     - ORM abstracts away the complexities of SQL queries and database interactions.
     - Developers work with objects and methods, not raw SQL.
   - **Security Improvements**:
     - ORM tools guard against SQL injection attacks.
     - They sanitise input and handle parameter binding automatically.
   - **Less Code to Write**:
     - ORM tools generate boilerplate code for CRUD (Create, Read, Update, Delete) operations.
     - Developers write less code compared to manual SQL queries.

All in all, ORM tools simplify data persistence, enhance security, and improve development efficiency by connecting object-oriented code with relational databases.

---

## R5	Document all endpoints for your API 

## Authentication Endpoints
   `url_prefix="/auth"`
### 1. Endpoint to register new users

   ```py
   @auth_bp.route("/register", methods=["POST"])
   ```
The user should input information for all columns to proceed  
`name`, `email`, `password`, `age`, `weight`, `height`, `gender` `is_admin`.  
serialised by the database  
 `id`, `date_joined`,

**Expected response**  
   - 201 created  
   - hashed password

--
### 2. Endpoint to login
   ```py
   @auth_bp.route("/login", methods=["POST"])
   ```
```json
{
  "email": "user@gmail.com",
  "password": "User1!"
}
```
**Validations:**  
- match `email` to existing or newly created user
- `Password`: must be at least 6 characters long; contain one or many digits, special characters, lowercase and uppercase letters. No space allowed.

**Expected response**  
   { "token": access_token }

--

## Profile Endpoints
`url_prefix="/profile"`
### 1. Endpoints to read user or users
Admin can access user profiles, user can access his/her own profile

```py
@profile_bp.route("/<int:user_id>", methods=["GET"])
```
**Expected response**  
Specific user filtered by id
```json
{
	"id": 5,
	"name": "Gussio Ratzz",
	"email": "ratzst4tz@gmail.com",
	"age": 20,
	"weight": 120,
	"height": 200,
	"gender": "M",
	"date_joined": "2024-03-23",
	"is_admin": false
}
```
```py
@profile_bp.route("/", methods=["GET"])
```
**Expected response**  
All existing users in user_table
```json
[
	{
		"id": 1,
		"name": "The Admin",
		"email": "admin@workoutwebAPI.com",
		... (Other Columns)
		"is_admin": true
	},
	{
      "id": 2,
		"name": "Gustavo Jimenez",
		"email": "gus.jim@workoutwebAPI.com",
		... (Other Columns)
		"is_admin": false
	},
	{
      "id": 3,
		"name": "Gussio Ratzz",
		"email": "ratzz@gmail.com",
		... (Other Columns)
		"is_admin": false
	},
]
```
--

### 2. Endpoint to delete user
- Admin can delete any profile
- Only the registered/logged in owner can delete their own profile
```py
@profile_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
```
**Expected response**  
- removal of expected profile filtered by the user_id
- return not found 404 if profile does not exist or forbidden 403 if the wrong user is trying to delete
--

### 2. Endpoint to edit user
```py
@profile_bp.route("/<int:user_id>", methods=["PATCH", "PUT"])
@jwt_required()
```
**Expected response**  
- Only the owner of the profile can edit the info within
- forbidden 403 if admin or the wrong user is trying to edit

--

## Routine Endpoints
   `url_prefix="/routines"`
### 1. Routine Endpoint - read all routines available or specific one
All users can have access to read all routines
```py
@routine_bp.route("/")
//
@routine_bp.route("/<int:routine_id>")
```
**Expected response**  
the routine should have all the information attached to it, like exercise(s) and its sets, reps, and goal

```json
{
	"id": 1,
	"name": "Chest",
	"description": "Description for Chest workout",
	"weekday": "Monday",
	"user": {
		"id": 2,
		"name": "Gustavo Jimenez",
		"age": 43,
		"weight": 68,
		"height": 170,
		"gender": "M"
	},
	"exercises": [
		{
			"id": 1,
			"name": "Bench Press",
			"category": "easy",
			"muscles": "Pectoralis major, Anterior deltoids, Triceps brachii",
			"description": "Description Bench Press",
			"user": {
				"name": "Gustavo Jimenez"
			},
			"sets_reps": [
				{
					"id": 1,
					"sets": 6,
					"reps": 4,
					"goal": "Strenght"
				}
			]
		}
	]
}
```
--
### 2. Routine Endpoint - Create routine
```py
@routine_bp.route("/", methods=["POST"])
@jwt_required()
```
All users can create new routines,
```json
{
	"name": "Don't skip Leg Day",
	"description": "Short Description for leg routine",
	"weekday": "Sunday"
}
```
**Expected response**  
if any of the 3 required fields are left empty or don't follow the validation a 400 error is returned
```json
{
	"id": 12,
	"name": "Don't skip Leg Day",
	"description": "Short Description for leg routine",
	"weekday": "Sunday",
	"user": {
		"id": 3,
		"name": "Gussio Ratzz",
		"age": 50,
		"weight": 120,
		"height": 200,
		"gender": "M"
	},
	"exercises": []
}
```

--

### 3. Routine Endpoint - Updated or edit existing routine
```py
@routine_bp.route("/<int:routine_id>", methods=["PATCH", "PUT"])
@jwt_required()
```
Only the owner or creator of the routine can edit,
```json
{
	"name": "Don't skip Leg Day", // can be updated of left as is
	"description": "Short Description for leg routine", // can be updated of left as is
	"weekday": "Sunday" // can be updated of left as is
}
```
**Expected response**  
if the owner of the routine did not follow the validation a 400 error is returned
```json
{
	"id": 12,
	"name": "Don't skip Leg Day", // updated or left as it was
	"description": "Short Description for leg routine", // updated or left as it was
	"weekday": "Sunday", // updated or left as it was
	"user": {
		"id": 3,
		"name": "Gussio Ratzz",
		"age": 50,
		"weight": 120,
		"height": 200,
		"gender": "M"
	},
	"exercises": []
}
```
--

### 4. Routine Endpoint - Delete
```py
@routine_bp.route("/<int:routine_id>", methods=["DELETE"])
@jwt_required()
```
Only the owner or creator of the routine can delete

**Expected response**  
- Deletion of the routine with specific routine_id  

**Errors**
- if the wrong owner of the routine is trying to delete a Forbidden 403 error is returned
- if the routine_id does not exist a 404 not found is returned


--

## Exercises Endpoints
   `url_prefix="/exercises"`
###21. Exercises Endpoint - Read
All users and Admin can access to read multiple exercises or a specific one filtered by the name 
```py
@exercise_only_bp.route("/<exercise_name>")
```

**Expected response**  
http://127.0.0.1:8888/exercises/Push-Ups  
A URL like this will return the below 
```json
{
	"id": 2,
	"name": "Push-Ups",
	"category": "easy",
	"muscles": "Pectoralis major, Anterior deltoids, Triceps brachii",
	"description": "Description Push-Ups",
	"user": {
		"name": "Gustavo Jimenez"
	},
	"routine": {
		"weekday": "Monday",
		"name": "Chest"
	},
	"sets_reps": [
		{
			"id": 2,
			"sets": 3,
			"reps": 20,
			"goal": "Tone"
		}
	]
}
```

```py
@exercise_only_bp.route("/")
```

**Expected response**  
http://127.0.0.1:8888/exercises/  
A generic URL returns all exercises available
```json
[
	{
		"id": 1,
		"name": "Bench Press",
		"category": "easy",
		"muscles": "Pectoralis major, Anterior deltoids, Triceps brachii",
		"description": "Description Bench Press",
		"user": {
			"name": "Gustavo Jimenez"
		},
		"routine": {
			"weekday": "Monday",
			"name": "Chest"
		},
		"sets_reps": [
			{
				"id": 1,
				"sets": 6,
				"reps": 4,
				"goal": "Strenght"
			}
		]
	},
	{
		"id": 2,
		"name": "Push-Ups",
		"category": "easy",
		"muscles": "Pectoralis major, Anterior deltoids, Triceps brachii",
		"description": "Description Push-Ups",
		"user": {
			"name": "Gustavo Jimenez"
		},
		"routine": {
			"weekday": "Monday",
			"name": "Chest"
		},
		"sets_reps": []
	}
]   
```
--

### 2. Exercise Endpoint - Create a new exercise in a routine
   The prefix from routines and prefix in exercises the route is like the below
   `url_prefix="/routines/<int:routine_id>/exercises")`
```py
@exercise_bp.route('/', methods=["POST"])
@jwt_required() 
```
- only the creator of the routine can create and add the exercise to it
- The owner of the routine inputs the data
```json
{
	"name": "Inclined Bench Press",
	"category": "Advanced",
	"muscles": "",
	"description": "Sit on a bench and rest your back..."
}
```
**Expected response**  
```json
{
	"id": 4,
	"name": "Inclined Bench Press",
	"category": "Advanced",
	"muscles": "",
	"description": "Sit on a bench and rest your back...",
	"user": {
		"name": "Gussio Ratzz"
	},
	"routine": {
		"weekday": "Sunday",
		"name": "Chest"
	},
	"sets_reps": []
}
```
**Errors**
- if the user is trying to create an exercise into a routine that is not his/hers a 403 Forbidden error will be returned
- if a user is creating an exercise into a routine that is non-existent a 404 Not found error is returned

--

### 3. Exercise Endpoint - Edit an exercise
   The prefix from routines and prefix in exercises the route is like the below
   `url_prefix="/routines/<int:routine_id>/exercises")`
```py
@exercise_bp.route('/<int:exercise_id>', methods=["PUT", "PATCH"])
@jwt_required()
```
- only the creator of the routine can edit the exercise
- The owner of the routine inputs the updated data
```json
{
	"name": "Declined Bench Press", // Updated column
	"muscles": "Pectoralis" // Updated column
}
```
**Expected response**  
```json
{
	"id": 4,
	"name": "Declined Bench Press",
	"category": "Advanced",
	"muscles": "Pectoralis",
	"description": "Sit on a bench and rest your back...",
	"user": {
		"name": "Gussio Ratzz"
	},
	"routine": {
		"weekday": "Sunday",
		"name": "Chest"
	},
	"sets_reps": []
}
```
**Errors**
- if a user is trying to edit an exercise into a routine that is not his/hers a 403 Forbidden error will be returned
- if the id of the exercise does not exist a 404 Not found error is returned

--

### 4. Exercise Endpoint - Delete an exercise
   The prefix from routines and prefix in exercises the route is like the below
   `url_prefix="/routines/<int:routine_id>/exercises")`
```py
@exercise_bp.route('/<int:exercise_id>', methods=["DELETE"])
@jwt_required()
```
- Only the creator of the routine can delete the exercise


**Expected response** 
```json
{
	{
	"message": "Bench Press exercise has been removed from Monday routine"
}
}
``` 
**Errors returned**

- if a user is trying to edit an exercise into a routine that is not his/hers a 403 Forbidden error will be returned

```json
{
	"error": "Only the creator can delete this exercise"
}
```

- if the id of the exercise does not exist a 404 Not found error is returned

```json
{
	"error": "This exercise does not exist in your Monday routine"
}
```
--
## Sets and Reps Endpoints
### 1. Sets and Reps Endpoint - Create and add sets and reps to an exercise
   The prefix from exercises and prefix in sets_reps, the route is like the below
   `url_prefix="/exercises/<int:exercise_id>/sets_and_reps")`
```py
@sets_reps_bp.route("/", methods=["POST"])
@jwt_required()
```
- Only the creator of the exercise can add sets and reps into and exercise

body_data
```json
{
	"sets": 1,
	"reps": 90,
	"goal": "Tone"
}
```

**Expected response** 
```json
{
	"id": 3,
	"sets": 1,
	"reps": 90,
	"goal": "Tone",
	"exercises": {
		"name": "Leg Press"
	},
	"user": {
		"name": "Gussio Ratzz",
		"email": "ratawp@gmail.com"
	}
}
``` 
**Errors returned**

- if the user is trying to add sets and reps into an exercise that already has them assigned a 409 Conflict error will is returned
- the below message is also displayed
```json
[
	{
		"error": "There are asigned sets and reps to 'Leg Press'"
	},
	{
		"Sets and Reps Assigned": "set: 1, repetitons: 90, goal: Tone"
	}
]
```
- if the user is not the owner or creator of the routine, the exercise cannot be added to ti
```json
{
	"error": "Only the creator of 'Upper Chest Gussio' routine can add exercises to it"
}
```

- if the id of the exercise does not exist a 404 Not found error is returned

```json
{
	"error": "This exercise does not exist in your Monday routine"
}
```

--
### 2. Sets and Reps Endpoint - update or edit sets and reps
   The prefix from exercises and prefix in sets_reps, the route is like the below
   `url_prefix="/exercises/<int:exercise_id>/sets_and_reps")`
```py
@sets_reps_bp.route("/<int:sets_reps_id>", methods=["PATCH", "PUT"])
@jwt_required()
```
- Only the creator of the routine and exercise can edit sets and reps

body_data
```json
{
	"sets": 2, // updated
	"reps": 12, // updated
	"goal": "Strength" // updated
}
```

**Expected response** 
```json
{
	"id": 3,
	"sets": 2,
	"reps": 12,
	"goal": "Strength",
	"exercises": {
		"name": "Leg Press"
	},
	"user": {
		"name": "Gussio Ratzz",
		"email": "ratawp@gmail.com"
	}
}
``` 
**Errors returned**

- if the wrong user is trying to edit sets and reps a forbidden 403 error is thrown
```json
{
	"error": "These sets and reps are associted to another user's exercise, you cannot modify it"
}
```

- if the exercise does not exist a 404 Not found is returned
```json
{
	"error": "Exercise not found"
}
```

- if the id of the exercise does not exist a 404 Not found error is returned

```json
{
	"error": "This exercise does not exist in your Monday routine"
}
```

- if the id of the sets and reps does not exist a 404 Not found error is returned
```json
{
	"error": "No sets and reps found with id 12"
}
```
--

### 3. Sets and Reps Endpoint - Delete
   The prefix from exercises and prefix in sets_reps, the route is like the below
   `url_prefix="/exercises/<int:exercise_id>/sets_and_reps")`
```py
@sets_reps_bp.route("/", methods=["DELETE"])
@jwt_required()
```
- Only the creator of the routine and exercise can delete sets and reps

**Expected response** 
```json
{
	"message": "sets and reps for 'name of the exericse' have been deleted"
}
``` 
**Errors returned**

- if the wrong user is trying to delete sets and reps a forbidden 403 error is thrown
```json
{
	"error": "Only the creator of 'name of the exericse' can delete its associted sets and reps"
}
```

- if sets and reps does not exist a 404 Not found is returned
```json
{
	"error": "Not found, sets or reps are not yet set up"
}
```

- if the id of the exercise does not exist a 404 Not found error is returned

```json
{
	"error": "This exercise does not exist in your Monday routine"
}
```

- if the id of the sets and reps does not exist a 404 Not found error is returned
```json
{
	"error": "No sets and reps found with id 'id number'"
}
```

---

## R6	An ERD for your app
![ERD](./docs/GustavoJimenez-Database_ERD.png)

## R7	Detail any third party services that your app will use

Sure, let's break down each of these third-party services:

### Flask:
Flask is a micro web framework for Python based on Werkzeug and Jinja2. It's lightweight and designed to make getting started with web development in Python easy. Flask provides tools, libraries, and patterns for building web applications, allowing developers to create web applications quickly and with less boilerplate code compared to some other frameworks.

#### Flask Blueprint:
A Flask Blueprint is a way to organise a group of related views, templates, and static files. It allows to modularise the application by dividing it into smaller, reusable components. Blueprints are particularly useful for structuring large applications or for creating reusable components that can be shared across multiple projects.

### Psycopg2:
Psycopg2 is a PostgreSQL adapter for the Python programming language. It allows Python code to interact with PostgreSQL databases. Psycopg2 provides a way to execute SQL commands, fetch data, and manage database connections from within Python code.

### Flask-JWT-Extended:
Flask-JWT-Extended is an extension for Flask that adds support for JSON Web Tokens (JWT) to Flask applications. JWTs are a compact, URL-safe means of representing claims to be transferred between two parties. They are commonly used for authentication and authorization in web applications.

- **jwt_required:**
`jwt_required` is a decorator provided by Flask-JWT-Extended. It is used to protect routes or endpoints in Flask applications by requiring a valid JWT to be present in the request headers. If a request is made to a route decorated with `jwt_required`, but the JWT is missing or invalid, Flask-JWT-Extended will return an error response.

**get_jwt_identity:**
`get_jwt_identity` is a function provided by Flask-JWT-Extended. It is used to retrieve the identity (i.e., the user or entity associated with the JWT) from the current request context. This function is commonly used within protected routes to obtain information about the authenticated user or entity.

### Marshmallow:
Marshmallow is a library for object serialization and deserialization in Python. It provides a simple and flexible way to convert complex data types, such as objects or dictionaries, into native Python data types that can be easily serialized to JSON or other formats.

- **fields:**
In Marshmallow, `fields` are used to define the structure of the data that will be serialized or deserialized. Marshmallow provides various field types, such as `StringField`, `IntegerField`, `BooleanField`, etc., which can be used to define the schema of the data.

- **validates:**
`validates` is a decorator provided by Marshmallow that is used to define custom validation logic for fields. By decorating a method with `@validates`, you can specify additional validation rules that should be applied when serializing or deserializing data.

- **marshmallow.validate Length, And, Regexp, OneOf:**
These are built-in validators provided by Marshmallow that can be used to enforce various validation rules on fields. For example:
- `Length` validator is used to ensure that a field's value has a specific length.
- `Regexp` validator is used to ensure that a field's value matches a specified regular expression pattern.
- `OneOf` validator is used to ensure that a field's value is one of a specified list of choices.

### datetime:
`datetime` is a module in Python's standard library that provides classes for manipulating dates and times. It allows developers to work with dates, times, and time intervals in a straightforward and efficient manner. The `datetime` module includes classes such as `datetime`, `date`, `time`, `timedelta`, etc., which can be used to represent and manipulate dates and times in Python code.

### sqlalchemy:
SQLAlchemy is an SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of high-level abstractions for working with SQL databases in Python, allowing developers to interact with databases using Python objects rather than raw SQL queries. SQLAlchemy supports multiple database backends and provides features such as database schema management, querying, and transaction handling.

- **sqlalchemy.exc:**
`sqlalchemy.exc` is a module within the SQLAlchemy library that contains exception classes for handling errors and exceptions related to database operations. This module provides a variety of exception classes that can be caught and handled by Python code when interacting with databases using SQLAlchemy. These exceptions can indicate errors such as database connection failures, integrity constraint violations, or syntax errors in SQL queries.

---

## R8	Describe your projects models in terms of the relationships they have with each other

In this kind of application, the `user` interacts with each and every table, since personal input is required to build each user's specific needs and constant adjustments in their fitness journey
1. **user_table**:
    - Represents users and contains information about them.
    - The `id` field serves as the `primary_key`.
    - Other fields include `name`, `email`, `password`, `date_joined`, `age`, `weight`, `height`, `gender`, and `is_admin`.
    - The `id` field is referenced as a foreign key in other tables.

- **User** table interacts with `sets_reps` table. While **sets** and **reps** have a broad range, the set values in **goal** help determining the actual purpose of the exercises these are assigned to.

- **User** table interacts with `exercises` table, bringing the user's key information like `gender` or `weight` to aid in the decision-making of suitable exercises

- User table has access to `routines` a table that consists of groups or of similar exercises based on `category` and `muscle`. Each **routine** could be assigned to a specific day of the week

2. **sets_reps**:
    - Stores data related to exercise sets and repetitions.
    - Contains fields like `id`, `user_id`, `exercise_id`, `sets`, `reps`, and `goal`.
    - The `id` field is the primary key.
    - The `user_id` field references the `id` in the `user_table`.
- **sets and reps** adds more data normalisation by adding its content to the selected exercise 
- The information in this table can be accessed and modified via the exercises. 

3. **exercise_table**:
    - Represents various exercises.
    - Fields include `id`, `name`, `category`, `muscles`, `description`, `user_id`, `routine_id`, and `sets_reps`.
    - The `id` field is the primary key.
    - The `user_id` field references the `id` in the `user_table`.
    - The `id` field is also referenced in the `sets_reps` table.
- Exercises and the information in it can be accessed and modified via routine_table
- Sets and reps is an integral part of exercises, since it provides key information to achieve the final goal 

4. **routine_table**:
    - Describes exercise routines.
    - Contains fields like `id`, `name`, `description`, `weekday`, and `user_id`.
    - The `id` field is the primary key.
    - The `user_id` field references the `id` in the `user_table`.
- Routines are the final view of the user, all the information contained in exercises and in sets and reps, giving shape to each routine created by the user
A user can create, modify, delete multiple routines, that user can also read or access other routines but cannot modify or delete

In summary, the relationships are as follows:
- Users (in `user_table`) can have multiple routines (in `routine_table`).
- Each routine can consist of various exercises created (in `exercise_table`).
- Exercise sets and repetitions (in `sets_reps`) are associated with specific exercises.

---

## R9 Discuss the database relations to be implemented in your application

1. **One-to-Many Relationship (User to Routines)**:
   - The `user` table has a one-to-many relationship with the `routines` table.
   - Each user can have multiple routines, but each routine belongs to only one user.
   - This relationship is established through the `user_id` foreign key in the `routines` table.

2. **One-to-Many Relationship (Routines to Exercise)**:
   - The `routines` table has a one-to-many relationship with the `exercise` table.
   - A routine can include multiple exercises, however an exercise can be part of one routine.
   - The `exercise` table acts as a junction table, connecting user and routine table.

3. **One-to-Many Relationship (User to Exercise)**:
   - The `user` table has another one-to-many relationship with the `exercise` table.
   - Each user can create multiple exercises, but each exercise belongs to only one user or routine.
   - This relationship is established through the `user_id` foreign key in the `exercise` table.

4. **OneAndOnlyOne-to-Many Relationship (Sets and Reps to Exercise)**:
   - The `sets_reps` table has a one-and-only-one-to-many relationship with the `exercise` table.
   - Many exercises can have one sets and reps, but one exercise can only have one set and reps.
   
---

## R10	Describe the way tasks are allocated and tracked in your project

**Initial stage - Planning**  
I started by planning the ERD of my API project and getting it approved.
I read the assignment once again, and laid it out in the `readme` file to give me an idea of the major points to complete, besides coding stage.

I have chosen Trello to organise my project. I will track the progress of this project by having `TO DO`, `DOING`, and `DONE` columns in which I can organise daily tasks or ongoing ones

In this project I will use some of git planning and tracking tools. After having created my repository, I can use `issues` and `milestones` to give another level of accuracy and certainty to the progress of my project

[My Trello Board - online](https://trello.com/invite/b/L1POEgYR/ATTI77cb88eeb89b34c00ae41ed565cfe93739935333/fitness-and-workout-manager)

![Trello 01](./docs/Trello_01.png)

![Trello 02](./docs/Trello_02.png)

![Trello 03](./docs/Trello_03.png)

![Trello 04](./docs/Trello_04.png)

![Trello 05](./docs/Trello_05.png)

![Trello 06](./docs/Trello_06.png)

![Trello 07](./docs/Trello_07.png)
