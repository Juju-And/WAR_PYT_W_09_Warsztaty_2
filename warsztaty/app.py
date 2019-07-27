from models.user import User
from persistance import create_connection

ctx = create_connection()


def test_user():
    user = User()
    user.username = 'Mati'
    user.email = "blabla@xd.omg"
    cursor = ctx.cursor()
    user.save_to_db(cursor)
    ctx.commit()


def load_users():
    all = User.load_all_users(ctx.cursor())
    for user in all:
        print(repr(user))


def load_single_user(user_id):
    # cursor = ctx.cursor()
    return User.load_user_by_id(ctx.cursor(), user_id)


# test_user()
# test_user()
# load_users()
print(load_single_user(15))
