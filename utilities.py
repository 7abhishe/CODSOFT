import random
import string
from faker import Faker

fake = Faker()

def generate_random_email():
    return f"test_{random.randint(1000, 9999)}@example.com"

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def generate_random_name():
    return fake.first_name()

def generate_random_lastname():
    return fake.last_name()
