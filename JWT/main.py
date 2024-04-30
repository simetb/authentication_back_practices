"""
    JWT Token Generator and Decodifier
    Example of JWT Token authentication with Python
"""
import jwt
import datetime

USER_ID = 145

# Define the info that you want to include in the token
payload = {
    'user_id': USER_ID,
    'username': 'exanmple',
    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # Expiration time
}

# Generate the JWT token  with a secret key
secret_key ='my_secret_key'
token = jwt.encode(payload, secret_key, algorithm='HS256')
print(token)

try:
    # Decodify the token
    decoded_payload = jwt.decode(token, secret_key, algorithms='HS256')
    print(decoded_payload)
except jwt.ExpiredSignatureError:
    print('Token expired')
except jwt.InvalidTokenError:
    print('Invalid token')


