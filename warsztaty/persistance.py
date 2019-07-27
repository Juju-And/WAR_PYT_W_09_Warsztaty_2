from psycopg2 import connect, OperationalError

def create_connection():
    username = "postgres"
    passwd = "coderslab"
    hostname = "localhost"  # lub "localhost"
    db_name = "messenger"
    try:
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        print("Połączenie udane.")
        return cnx
    except OperationalError:
        print("Nieudane połączenie.")