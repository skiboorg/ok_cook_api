from decimal import *
from user.models import *


def calcRefBonuses(user,amount):
    top_user_amount = Decimal(amount * 0.1)
    next_user_amount = Decimal(amount * 0.05)
    first_line = UserRefferalFirstLine.objects.filter(users__id__in=[user.id])
    second_line = UserRefferalSecondLine.objects.filter(users__id__in=[user.id])
    third_line = UserRefferalThirdLine.objects.filter(users__id__in=[user.id])
    if first_line:
        # print('first_line',first_line)
        top_user = first_line.first().user
        top_user.ref_bonuses += top_user_amount

        top_user.save(update_fields=['ref_bonuses'])
    if second_line:
        # print('first_line',first_line)
        next_level_user = second_line.first().user
        next_level_user.ref_bonuses += next_user_amount

        next_level_user.save(update_fields=['ref_bonuses'])
    if third_line:
        # print('first_line',first_line)
        next_level_user = third_line.first().user
        next_level_user.ref_bonuses += next_user_amount

        next_level_user.save(update_fields=['ref_bonuses'])
