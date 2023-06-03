from flask import Flask, redirect, request
import geoip2.database

app = Flask(__name__)

ip_address_map = {
    'LK': '20.51.237.16',
    'US': '20.51.237.16'
}

@app.route('/register', methods=['POST'])
def register_endpoint():
    # Get the data from the request
    data = request.json

    # Validate the data
    if 'location' not in data or 'ip_address' not in data:
        return 'Invalid data', 400

    location = data['location']
    ip_address = data['ip_address']

    # Update the IP address map
    ip_address_map[location] = ip_address

    return 'IP address registered successfully', 200

# Load the GeoIP2 database
geoip_database = geoip2.database.Reader('/home/azureuser/GeoLite2-City.mmdb')

@app.route('/publish', methods=['POST'])
def original_endpoint1():
    # Process the incoming data if needed

    # Get the user's IP address from the request
    user_ip = request.remote_addr
    # user_ip="103.1.176.0"
    # user_ip="175.157.74.223"
    print("ip: ",user_ip)

    try:
        # Get the user's location based on the IP address
        response = geoip_database.city(user_ip)
        # print("res: ",response)
        location = response.country.iso_code
        # print("loc: ",location)
    except geoip2.errors.AddressNotFoundError:
        # Handle the case when the IP address is not found in the GeoIP database
        return 'Location not found', 404

    # Retrieve the corresponding IP address from the hashmap based on the location
    new_ip_address = ip_address_map.get(location)
    # print("new: ",new_ip_address)
    if new_ip_address:
        # Perform the redirect
        new_url = f'http://{new_ip_address}:8081/publish'
        return redirect(new_url, code=308)
    else:
        # Handle the case when the location is not found in the hashmap
        return 'Location not found', 404

@app.route('/orderInfo', methods=['GET'])
def original_endpoint2():
    # Process the incoming data if needed

    # Get the user's IP address from the request
    user_ip = request.remote_addr

    try:
        # Get the user's location based on the IP address
        response = geoip_database.city(user_ip)
        location = response.country.iso_code
    except geoip2.errors.AddressNotFoundError:
        # Handle the case when the IP address is not found in the GeoIP database
        return 'Location not found', 404

    # Retrieve the corresponding IP address from the hashmap based on the location
    new_ip_address = ip_address_map.get(location)

    if new_ip_address:
        # Perform the redirect
        new_url = f'http://{new_ip_address}:8081/orderInfo'
        return redirect(new_url, code=308)
    else:
        # Handle the case when the location is not found in the hashmap
        return 'Location not found', 404

if __name__ == '__main__':
    app.run(debug=True, port=8081, host='0.0.0.0')
