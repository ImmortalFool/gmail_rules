from mysql.connector import connect, Error

DB_NAME = "HAPPYFOX"

def check_database(cursor):
    try:
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        if cursor.fetchone():
            print(f"Database '{DB_NAME}' already exists.")
        else:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created.")
    except Error as e:
        print(f"An error occurred while checking/creating the database: {e}")

def create_tables(cursor):
    try:
        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email_id VARCHAR(255) UNIQUE,
                sender VARCHAR(255) NOT NULL, 
                subject VARCHAR(255),
                date DATE,
                is_read BOOL,
                folders VARCHAR(255)
            )
        """)

        # Create labels table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS labels (
                id INT AUTO_INCREMENT PRIMARY KEY,
                label VARCHAR(100) UNIQUE
            )
        """)
        print("Tables created successfully.")
    except Error as e:
        print(f"An error occurred while creating tables: {e}")

def database_connection():
    try:
        # Connect to MySQL
        connection = connect(host="localhost", user="root", password="admin")
        cursor = connection.cursor()
        check_database(cursor)
        cursor.execute(f"USE {DB_NAME}")
        create_tables(cursor)
        return connection

    except Error as e:
        # Raise an exception if an error occurs
        raise ConnectionError(f"An error occurred while connecting to MySQL: {e}")


def insert_into_messages(messages):
    # try:
    # Connect to MySQL
    connection = database_connection()
    cursor = connection.cursor()

    # Define the SQL query for inserting messages
    insert_messages_query = """
    INSERT INTO messages
    (email_id, sender, subject, date, is_read, folders)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    # Execute the query for each message in the list
    cursor.executemany(insert_messages_query, messages)
    connection.commit()
    print("Messages inserted successfully into 'messages' table.")

    # except Error as error:
    #     print("Failed to insert messages into 'messages' table:", error)
    #
    # finally:
    #     # Close cursor and connection
    #     if connection.is_connected():
    #         cursor.close()
    connection.close()

def insert_into_labels(labels):
    try:
        # Connect to MySQL
        connection = database_connection()
        cursor = connection.cursor()

        # Get list of label names
        label_names = list(labels.keys())

        # Define the SQL query for inserting labels
        insert_labels_query = """
        INSERT INTO labels
        (label)
        VALUES (%s)
        """

        # Execute the query for each label name in the list
        for label_name in label_names:
            cursor.execute(insert_labels_query, (label_name,))
            connection.commit()
        print("Labels inserted successfully into 'labels' table.")

    except Error as error:
        print("Failed to insert labels into 'labels' table:", error)

    finally:
        # Close cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
