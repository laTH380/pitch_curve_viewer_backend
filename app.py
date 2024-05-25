from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Home Page!'

@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'

@app.route('/data', methods=['POST'])
def process_data():
    data = request.get_json()
    return jsonify({'received': data})

if __name__ == '__main__':
    app.run(debug=True)
