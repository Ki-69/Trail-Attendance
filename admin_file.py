import mysql.connector


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

    def database_exists(self):
        try:
            # Establish a connection to MySQL Server
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

            # If the connection is successful, the database exists
            return True

        except mysql.connector.Error as e:
            # If the connection fails, the database doesn't exist
            return False

        finally:
            # Close the connection
            if self.conn:
                self.conn.close()

    def create_database(self):
        try:
            # Establish a connection to MySQL Server
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
            )

            # Create a cursor object using the cursor() method
            self.cursor = self.conn.cursor()

            # SQL statement to create a new database
            create_database_query = f"CREATE DATABASE {self.database}"

            # Execute the SQL statement using the execute() method of the cursor object
            self.cursor.execute(create_database_query)

            print(f"Database '{self.database}' created successfully!")

        except mysql.connector.Error as e:
            print(f"Error creating the database: {e}")

        finally:
            # Close the cursor and connection
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def create_table_for_class(self):
        try:
            obj.connect()
            class_name = input(
                "enter the class name to create a table: (example = class12a): "
            )
            query = f"create table {class_name} (Student_name varchar(255) not null, Roll_no int not null); "
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            tables_names = obj.store_table_names()
            print(tables_names)
            choice = input(
                "do you want to rerun the program or move onto next function with a table of your choosing: y/n: "
            )
            if choice == "y":
                obj.create_table_for_class()
            else:
                pass

    def store_table_names(self):
        obj.connect()
        query = "show tables;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        store = []
        for i in result:
            store.append(i[0])
        return store


obj = UserAuthenticator("localhost", "root", "1234", "newattendance")
obj.database_exists()
obj.create_database()
obj.create_table_for_class()
