from typing import Tuple

from django.db import transaction

from contacts_app.models import User


def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first()

    if user:
        return user, False
    username = extra_data["first_name"]
    return user_create(email=email, username=username, **extra_data), True
