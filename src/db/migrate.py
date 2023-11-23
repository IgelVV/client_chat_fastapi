from connector import get_connection


connection = get_connection()

with connection:
    with connection.cursor() as cursor:
        sql = """
        CREATE TABLE IF NOT EXISTS User(
            id INT NOT NULL AUTO_INCREMENT, 
            username VARCHAR(50) NOT NULL, 
            password VARCHAR(64) NOT NULL, 
            is_admin BOOLEAN NOT NULL,
            PRIMARY KEY (id),
            UNIQUE (username)
        )
        """
        cursor.execute(sql)

    connection.commit()
    print("User table exists.")

    with connection.cursor() as cursor:
        sql = """
        CREATE TABLE IF NOT EXISTS Chat(
            id INT NOT NULL AUTO_INCREMENT, 
            customer_id INT, 
            admin_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY (customer_id) REFERENCES User(id),
            FOREIGN KEY (admin_id) REFERENCES User(id)
        )
        """
        cursor.execute(sql)

    connection.commit()
    print("Chat table exists.")

    with connection.cursor() as cursor:
        sql = """
        CREATE TABLE IF NOT EXISTS Message(
            id INT NOT NULL AUTO_INCREMENT, 
            chat_id INT, 
            datetime DATETIME,
            text TEXT(500),
            PRIMARY KEY (id),
            FOREIGN KEY (chat_id) REFERENCES Chat(id)
        )
        """
        cursor.execute(sql)

    connection.commit()
    print("Message table exists.")

    with connection.cursor() as cursor:
        sql = """
            INSERT IGNORE INTO User(username, password, is_admin) 
            VALUES ('admin', 'password', true)
            """
        cursor.execute(sql)

    connection.commit()
    print("admin user is created.")

    print("Migration is completed.")


# select LENGTH(SHA2(CONVERT('asasdasd' USING utf8), 256));