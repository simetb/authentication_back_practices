"""
    Token Base 64 Encoding
"""
import base64

# Replace 'username' and 'password' with your own credentials
# username = username
# password = password
username = 'username'
password = 'password'

# Concatenate username and password with a colon
credentiales= "{}:{}".format(username, password)

correct = b'dXNlcm5hbWU6cGFzc3dvcmQ='

# Encode credentials using base64 encoding
encoded_credentials = base64.b64encode(credentiales.encode('utf-8'))

if(encoded_credentials == correct):
    print("Credentials are correct!")
else:
    print("Credentials are incorrect!")