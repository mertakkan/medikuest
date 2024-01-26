### Instructions to run the project:

1. Change MySQL passwords in files:
     DatabaseQuery.py
     MedicalDatabaseCreate.py
     UserTableCreate.py
2. Uncomment line:
   14: db_cursor.execute("CREATE DATABASE MedicalDatabase") inside MedicalDatabaseCreate.py
   This line can be under comment again after the file was executed, this is needed to create the MySQL database. It is enough for the file to be executed once.
3. Run 'python MedicalDatabase.py' from terminal in 'backend' folder.
4. Run 'python UserTableCreate.py' from terminal in 'backend' folder. You may edit users in user.csv.
5. Run 'npm install' from main 'medikuest' folder to install all the necessary node modules for the project.
6. Run 'python app.py' from terminal in 'backend' folder.
7. Run 'npm start' from main 'medikuest' folder.
8. You may login using 'admin' '12345' or create a new user.

## Available Scripts

In the project directory, you can run:

### 'npm start'

This command should be executed from the 'medikuest' folder of the project.

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### 'python app.py'

This command should be executed from the 'backend' folder located in the project folder.
This allows the app to connect to the backend part of the project through Flask.
