"""
    Example of setting and getting a cookie in Flask
    Cookies authentication
"""
import json
from flask import Flask, request, make_response

app = Flask(__name__)

# Route to set a cookie and return the cookie value
@app.route('/set_cookie', methods=['GET'])
def set_cookie():
    data_to_store = {'user_name':'example', 'user_id': 1234}
    json_data = json.dumps(data_to_store)
    resp = make_response("Cookie was set correctly", 200)
    resp.set_cookie('my_cookie', json_data)
    return resp

# Route to get the cookie value and return it
@app.route('/get_cookie', methods=['GET'])
def get_cookie():
    cookie_value = request.cookies.get('my_cookie')
    if cookie_value:
        json_data = json.loads(cookie_value)
        return "The cookie value is: " + json_data['user_name'] + " " + str(json_data['user_id'])
    else:
        return "The cookie does not exist"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)