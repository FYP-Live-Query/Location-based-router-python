from flask import Flask, redirect, request
import geoip2.database

app = Flask(__name__)

ip_address_map = {
    'LK': '10.8.100.246',
    'US': '20.171.111.32'
}

# Load the GeoIP2 database
geoip_database = geoip2.database.Reader('path/to/GeoIP2-City.mmdb')

@app.route('/publish', methods=['POST'])
def original_endpoint1():
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
        new_url = f'http://{new_ip_address}:8081/publish'
        return redirect(new_url, code=308)
    else:
        # Handle the case when the location is not found in the hashmap
        return 'Location not found', 404

@app.route('/time', methods=['GET'])
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
        new_url = f'http://{new_ip_address}:8081/time'
        return redirect(new_url, code=308)
    else:
        # Handle the case when the location is not found in the hashmap
        return 'Location not found', 404

if __name__ == '__main__':
    app.run(debug=True, port=8081, host='0.0.0.0')
