from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per day", "3 per second"])#Limter requires key_func to tell it how to target people
#Using get_remote_address tells key_func to target based on IP addresses