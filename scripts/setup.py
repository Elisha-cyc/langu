from backend.database.connection import get_connection
from backend.database.models import( CREATE_USERS_TABLE,  CREATE_LESSONS_TABLE, GET_TABLES, CREATE_PROGRESS_TABLE)


def setup_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(CREATE_USERS_TABLE)

    cursor.execute(CREATE_LESSONS_TABLE)

    cursor.execute(CREATE_PROGRESS_TABLE)

    connection.commit()

    cursor.execute(GET_TABLES)



    tables = cursor.fetchall()


    print("table in Database ")

    for table in tables:
        print(table[0])



    connection.close()



if __name__ == "__main__":
    setup_database()