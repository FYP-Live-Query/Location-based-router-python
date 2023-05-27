from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/publish', methods=['POST'])
def original_endpoint1():
    # Process the incoming data if needed

    # Perform the redirect
    new_ip_address = 'http://20.51.237.16:8081/publish'
    return redirect(new_ip_address, code=308)

@app.route('/time', methods=['GET'])
def original_endpoint2():
    # Process the incoming data if needed

    # Perform the redirect
    new_ip_address = 'http://20.51.237.16:8081/time'
    return redirect(new_ip_address, code=308)

if __name__ == '__main__':
    app.run(debug=True, port=8081,host='0.0.0.0')