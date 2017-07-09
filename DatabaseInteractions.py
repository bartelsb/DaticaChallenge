import sqlite3

database_file = './user_database.sqlite'


def create_database():

    # Connecting to the database file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Creating ths user table
    c.execute('CREATE TABLE user_table '
              '(p_ID INTEGER PRIMARY KEY AUTOINCREMENT, '
              'username TEXT NOT NULL UNIQUE, '
              'password TEXT NOT NULL, '
              'salt TEXT NOT NULL, '
              'additional_info TEXT, '
              'is_admin BOOLEAN)')

    # Committing changes and closing connection
    conn.commit()
    conn.close()


def create_user(username, password, salt, additional_info, is_admin):

    # Connecting to the database file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    params = (username, password, salt, additional_info, is_admin)

    c.execute("INSERT OR IGNORE INTO user_table VALUES (NULL, ?, ?, ?, ?, ?)", params)

    # Committing changes and closing connection
    conn.commit()
    conn.close()


def delete_user(username):

    # Connecting to the database file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    params = username,

    c.execute("DELETE FROM user_table WHERE username=?)", params)

    # Committing changes and closing connection
    conn.commit()
    conn.close()


def update_user(username, additional_info):

    # Connecting to the database file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    params = additional_info, username

    c.execute("UPDATE user_table SET additional_info=? WHERE username=?", params)

    # Committing changes and closing connection
    conn.commit()
    conn.close()


def retrieve_user(username):

    # Connecting to the database file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    params = username,

    c.execute("SELECT * FROM user_table WHERE username=?", params)
    user = c.fetchone()

    # Closing connection
    conn.close()
    return user
