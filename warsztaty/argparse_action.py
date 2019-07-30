from models.user import User
from persistance import create_connection
from clcrypto import password_hash
import argparse

ctx = create_connection()

parser = argparse.ArgumentParser(
    description='This is a PyMOTW sample program',
)


def require_len(length):
    def checked_len(password):
        if len(password) >= length:
            value = password
            return value
        else:
            msg = "Too short password"
            raise argparse.ArgumentTypeError(msg)

    return checked_len


parser.add_argument('-u', action='store',
                    dest="user_name",
                    help='Insert user name')

parser.add_argument('-m', action='store',
                    dest="user_email",
                    help='Insert users email')

parser.add_argument('-n', type=require_len(8), action='store',
                    dest="new_password",
                    help='Insert new password')

parser.add_argument('-e', action='store',
                    dest="modify_user",
                    help='Insert user name to modify')

parser.add_argument('-p', type=require_len(8), action='store',
                    dest="user_password",
                    help='Insert your password')

parser.add_argument('-l', action='store',
                    dest="users_list",
                    help='Require to list all users')

parser.add_argument('-d', action='store',
                    dest="delete_user",
                    help='Enter username to delete')

results = parser.parse_args()


# print(repr(results))


# print('simple_value1     = {!r}'.format(results.simple_value1))
# print('simple_value2     = {!r}'.format(results.simple_value2))

def add_user():
    user = User()
    user.username = results.user_name
    user.email = results.user_email
    user.set_password(results.user_password, None)
    cursor = ctx.cursor()
    user.save_to_db(cursor)
    ctx.commit()


#
#
# add_user()


# Jeśli użytkownik wprowadził parametry -u oraz -p, ale nie wprowadził parametru -e ani –d,
# sprawdzamy, czy użytkownik o takim emailu istnieje, a jeśli nie, to zakładamy użytkownika
# i nadajemy mu hasło. Jeśli użytkownik istnieje, zgłaszamy błąd.

def user_and_password():
    user_password = User.load_user_by_name_and_pass(ctx.cursor(), results.user_name, results.user_password)
    if user_password and not results.delete_user and not results.modify_user:
        return "User already exists, maybe you meant to delete '-d' or modify '-e'?"
    elif not user_password and not results.delete_user and not results.modify_user:
        add_user()
        return "User {} was added to the database".format(results.user_name)
    elif user_password and results.modify_user and not results.delete_user:
        User.update_password(ctx, password_hash(results.new_password, None), results.user_name)
        # print(results.new_password)
        # print(password_hash(results.new_password, None))
        return "Password successfully changed!"
    elif user_password and results.delete_user and not results.modify_user:
        User.delete_by_username(ctx.cursor(), results.user_name)
        return "User {} was deleted".format(results.user_name)
    elif not results.user_password or not results.user_name:
        return "User password or user name is missing, fill it to use the function"


print(user_and_password())
