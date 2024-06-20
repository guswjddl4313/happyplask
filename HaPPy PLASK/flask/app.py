from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps
from cryptography.fernet import Fernet
import requests, re, secrets, pickle, base64


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

INFO = ['userid', 'role']
key = Fernet.generate_key()

def access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'can_access_secret' in session and session['can_access_secret']:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return decorated_function


def filter_sqli(data):
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    return pattern.match(data) is not None


def generate_key():
    php_content = f'<?php\n    $key = "{key.decode()}";\n?>\nyou can\'t open this file'

    with open('key.php', 'w') as key_file:
        key_file.write(php_content)

    files = {'file': open('key.php', 'rb')}
    php_response = requests.post('http://php/upload.php', files=files)	


@app.route('/')
def index():
    generate_key()
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def submit():
    pw = request.args.get('pw')

    if not pw:
        return jsonify({'error': 'Not entered'}), 400

    if not filter_sqli(pw):
        return jsonify({'error': 'Don\'t try SQLI'}), 400

    try:
        php_response = requests.get('http://php/index.php?' + request.query_string.decode())
        print(f"response : {php_response}")
        if 'Login Success' in php_response.text:
            session['can_access_secret'] = True
            return redirect(url_for('admin'))
        else :
            return php_response.text

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/admin', methods=['GET', 'POST'])
@access_required
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    elif request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            info = {}
            for field in INFO:
                info[field] = request.form.get(field, '')

            keyf = Fernet(key)
            serialized_data = pickle.dumps(info)
            encrypted_data = keyf.encrypt(serialized_data)
            data = base64.b64encode(encrypted_data).decode('utf8')

            data_id = secrets.token_hex(16)
            with open(f'{data_id}.data', 'w') as file:
                file.write(data)

            files = {'file': open(f'{data_id}.data', 'rb')}
            try:
                php_response = requests.post('http://php/upload.php', files=files)
                if php_response.status_code == 200:
                    return render_template('admin.html', created_data=data, message='File uploaded successfully')
                else:
                    return render_template('admin.html', created_data=data, error='Failed to upload file')
            except Exception as e:
                return render_template('admin.html', created_data=data, error=f'Error occurred: {e}')

        elif action == 'check':
            session_data = request.form.get('session_data', '')
            try:
                keyf = Fernet(key)
                decode_data = base64.b64decode(session_data)
                decrypted_data = keyf.decrypt(decode_data)
                info = pickle.loads(decrypted_data)
                return render_template('admin.html', checked_info=info)
            except Exception as e:
                return render_template('admin.html', error=str(e))


@app.route('/data', methods=['GET'])
@access_required
def data():
    page = request.args.get('page')
    try:
        list_response = requests.get('http://php/data_main.php?' + request.query_string.decode())
        return list_response.text
    except Exception as e:
        return render_template('data_main.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
