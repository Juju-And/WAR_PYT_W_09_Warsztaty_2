import sys
import argparse

from warsztaty.persistance import create_connection
from warsztaty.models.user import User

sys.path.insert(0, '/home/Juju-And/WAR_PYT_W_09_Warsztaty_2')


connection = create_connection()
cursor = connection.cursor()

parser = argparse.ArgumentParser(description="Aplikacja do zarządzania użytkownikami")

parser.add_argument(
    '--list',
    action='store_true',
    help='Funkcja listująca wszystkich użytkowników',
    dest='list_all_users'
)

parser.add_argument('--version', action='version',
                    version='%(prog)s 1.0')

result = parser.parse_args()

if result.list_all_users:
    print(User.load_all_users(cursor))

connection.close()
