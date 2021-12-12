from random import choices
import string


def create_random_string(digits=False, num=4):
    if not digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string

def updateRefferals():
    from user.models import User, UserRefferalFirstLine, UserRefferalSecondLine, UserRefferalThirdLine
    """Поиск запись всех линий реффералов для всех пользователей"""


    all_users = User.objects.filter(is_active=True)

    for top_user in all_users:  # берем каждого юзера и получаем его собсвенный реф код
        top_user_own_ref_code = top_user.own_ref_code

        first_line_users = all_users.filter(
            used_ref_code=top_user_own_ref_code)  # фильтруем всех пользователей по реф.коду и получам первую линию
        second_line_users = []
        third_line_users = []

        for first_line_user in first_line_users:  # берем каждого юзера из первой линии и получаем его собсвенный реф код
            first_line_user_own_ref_code = first_line_user.own_ref_code
            second_line_users_array = []
            users_qs = all_users.filter(used_ref_code=first_line_user_own_ref_code)
            second_line_users_array.append(list(map(lambda user: user, users_qs)))
            for row in second_line_users_array:
                for item in row:
                    second_line_users.append(item)

            for second_line_user in second_line_users:
                second_line_user_own_ref_code = second_line_user.own_ref_code
                third_line_users_array = []
                users_qs = all_users.filter(used_ref_code=second_line_user_own_ref_code)
                third_line_users_array.append(list(map(lambda user: user, users_qs)))
                for row in third_line_users_array:
                    for item in row:
                        if not item in third_line_users:
                            third_line_users.append(item)

        first_line_user_obj, created_fl = UserRefferalFirstLine.objects.get_or_create(user=top_user)
        second_line_user_obj, created_sl = UserRefferalSecondLine.objects.get_or_create(user=top_user)
        third_line_user_obj, created_tl = UserRefferalThirdLine.objects.get_or_create(user=top_user)

        first_line_users_list = list(map(lambda user: user.id, first_line_users))
        second_line_users_list = list(map(lambda user: user.id, second_line_users))
        third_line_users_list = list(map(lambda user: user.id, third_line_users))

        first_line_user_obj.users.clear()
        first_line_user_obj.users.add(*first_line_users_list)

        second_line_user_obj.users.clear()
        second_line_user_obj.users.add(*second_line_users_list)

        third_line_user_obj.users.clear()
        third_line_user_obj.users.add(*third_line_users_list)
