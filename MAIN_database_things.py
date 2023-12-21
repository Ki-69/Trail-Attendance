from kivy.clock import Clock
import mysql.connector
from datetime import datetime
import csv


class UserAuthenticator:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.conn.cursor()
            return True
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            return False

    def authenticate_user(
        self, class_name="error in name", pass_word="error in password"
    ):
        valid_username = obj.store_table_names()
        valid_password = "parkar"
        while True:
            # Prompt the user for input
            input_username = class_name
            input_password = pass_word

            # Check if the entered username and password are valid
            if input_username in valid_username and input_password == valid_password:
                obj.connect()
                show_assigned_table = (
                    """select Roll_no, Student_name from {};  """.format(input_username)
                )
                self.cursor.execute(show_assigned_table)
                data = self.cursor.fetchall()

                store = []
                for i in data:
                    store.append(i)
                return store
                # break  # Exit the loop if authentication is successful
            else:
                return "Authentication failed. Please check your username and password. Retry."

    def add_columns(self):
        current_day_of_week = datetime.now().weekday()
        list_of_tables_in_database = obj.store_table_names()
        if current_day_of_week != 5 and current_day_of_week != 6:
            for i in list_of_tables_in_database:
                current_date = datetime.now().strftime("%Y_%m_%d")
                query = "alter table {} add {} varchar(255);".format(
                    i,
                    current_date,
                )
                self.cursor.execute(query)
                self.conn.commit()

    def mark_all_present(self, class_name):
        # Establish a database connection and update the attendance status
        self.connect()  # Make sure you have a method to connect to the database

        current_day_of_week = datetime.now().weekday()
        if current_day_of_week != 5 and current_day_of_week != 6:
            current_date = datetime.now().strftime("%Y_%m_%d")
        query = f"update {class_name} set {current_date}='Present';"
        self.cursor.execute(query)
        self.conn.commit()

    def custome_marking(self, class_name, student_list):
        obj.connect()

        current_day_of_week = datetime.now().weekday()
        if current_day_of_week != 5 and current_day_of_week != 6:
            current_date = datetime.now().strftime("%Y_%m_%d")

        valid_username = class_name
        for i in student_list:
            query = f"""UPDATE {valid_username} SET {current_date}="Absent" WHERE Roll_no={i};"""

            self.cursor.execute(query)
            self.conn.commit()

    def create_table_for_class(self, class_name):
        obj.connect()
        # class_name = input("enter the class name: (example = class12a): ")
        query = f"create table {class_name} (Student_name varchar(255) not null, Roll_no int not null); "
        self.cursor.execute(query)
        self.conn.commit()

    def store_table_names(self):
        obj.connect()
        query = "show tables;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        store = []
        for i in result:
            store.append(i[0])
        return store

    def add_data_into_tables(self, path, classname):
        # csv_file_path = input("enter the csv file path: ")
        obj.connect()
        class_name = classname

        with open(path, "r") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                student_name, roll_no = row
                query = (
                    "INSERT INTO {} (Student_name, Roll_no) VALUES (%s, %s);".format(
                        class_name
                    )
                )
                values = (student_name, int(roll_no))
                self.cursor.execute(query, values)
                self.conn.commit()

    def add_individual_chunks_database(self, classname, studentname, rollno):
        class_name = classname
        student_name = studentname
        roll_no = rollno

        obj.connect()
        query = "INSERT INTO {} (Student_name, Roll_no) VALUES (%s, %s);".format(
            class_name
        )
        values = (student_name, int(roll_no))
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_data(self, classname, rollno):
        obj.connect()
        for i in rollno:
            query = f"""delete from {classname} where Roll_no = {i} ;"""
            self.cursor.execute(query)
            self.conn.commit()

    def delete_all(self, classname):
        obj.connect()
        query = f"""DELETE FROM {classname} where Roll_no is not null ;"""
        self.cursor.execute(query)
        self.conn.commit()


def scheduled_task(dt):
    current_time = datetime.datetime.now().time()
    if current_time.hour == 9 and current_time.minute == 0:
        # Execute your task at 09:00
        try:
            # Your task function here, e.g., obj.add_columns()
            pass
        except Exception as e:
            # Handle exceptions here (logging, error reporting, etc.)
            print(f"Error occurred: {e}")


# Schedule the task using Kivy's Clock
Clock.schedule_interval(scheduled_task, 14400)  # Check every 4 hours

# Note: Change the interval to a more appropriate value depending on the required precision


# Create an instance of the UserAuthenticator class
obj = UserAuthenticator("localhost", "root", "1234", "attendance")
obj.authenticate_user()
# obj.add_columns()
