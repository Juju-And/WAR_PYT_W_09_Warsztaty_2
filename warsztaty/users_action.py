from models.user import User
from persistance import create_connection
from clcrypto import password_hash
import argparse

ctx = create_connection()

parser = argparse.ArgumentParser(
    description='This is a messenger',
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


parser.add_argument('-u', '--user', action='store',
                    dest="user_name",
                    help='Insert user name')

parser.add_argument('-m', '--mail', action='store',
                    dest="user_email",
                    help='Insert users email')

parser.add_argument('-n', '--new-pass', type=require_len(8), action='store',
                    dest="new_password",
                    help='Insert new password')

parser.add_argument('-e', '--edit', action='store',
                    dest="modify_user",
                    help='Insert user name to modify')

parser.add_argument('-p', '--password', type=require_len(8), action='store',
                    dest="user_password",
                    help='Insert your password')

parser.add_argument('-l', '--list', action='store_true',
                    dest="users_list",
                    help='Require to list all users')

parser.add_argument('-d', '--delete', action='store',
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

# add_user()


def user_and_password():
    correct_user_password = User.load_user_by_name_and_pass(ctx.cursor(), results.user_name, results.user_password)
    if not results.user_password \
            and not results.delete_user \
            and not results.modify_user \
            and not results.users_list:
        # return 'No argument was added, try to use "-h/--help"'
        return parser.print_help()
    elif correct_user_password \
            and not results.delete_user \
            and not results.modify_user \
            and not results.users_list:
        return "User already exists, maybe you meant to delete '-d' or modify '-e'?"
    elif results.user_name and results.user_password \
            and not correct_user_password \
            and not results.delete_user \
            and not results.modify_user:
        add_user()
        return "User {} was added to the database".format(results.user_name)
    elif correct_user_password and results.modify_user \
            and not results.delete_user:
        User.update_password(ctx, password_hash(results.new_password, None), results.user_name)
        # print(results.new_password)
        # print(password_hash(results.new_password, None))
        return "Password successfully changed!"
    elif correct_user_password and results.delete_user \
            and not results.modify_user:
        User.delete_by_username(ctx.cursor(), results.user_name)
        return "User {} was deleted".format(results.user_name)
    elif not results.user_password \
            or not results.user_name:
        return "User password or user name is missing, fill it to use the function"
    elif correct_user_password and results.users_list:
        users = User.load_all_users(ctx.cursor())
        for user in users:
            print(user)




print(user_and_password())
