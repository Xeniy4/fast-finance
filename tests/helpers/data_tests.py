import random
import string

import faker


def gen_random_amount(min_value: int, max_value: int) -> int:
    return random.randint(min_value, max_value)


def get_random_name() -> str:
    fake = faker.Faker()
    name = fake.first_name()
    return name


def gen_random_str(length: int = 20) -> str:
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(length)
    )
