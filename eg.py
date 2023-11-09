from flask import Flask, render_template, redirect, url_for, session, request
import requests
import json

app = Flask(__name__)
app.secret_key = 'secret_key'

credentials_json = """
{
    "web": {
        "client_id": "21211028908-hpvf2goio2ogmvm84dhj8i56ci6ef6md.apps.googleusercontent.com",
        "project_id": "thermal-outlet-404610",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["http://localhost:5000/auth/callback"]
    }
}
"""
credentials = json.loads(credentials_json)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = (
        f"{credentials['web']['auth_uri']}?client_id={credentials['web']['client_id']}&"
        f"redirect_uri={credentials['web']['redirect_uris'][0]}&response_type=code&scope=email&prompt=consent"
    )
    return redirect(auth_url)

@app.route('/auth/callback')
def authorized():
    code = request.args.get('code')

    if not code:
        return 'Access denied: Authorization code not received.'

    token_url = credentials['web']['token_uri']
    token_data = {
        'code': code,
        'client_id': credentials['web']['client_id'],
        'client_secret': credentials['web']['client_secret'],
        'redirect_uri': credentials['web']['redirect_uris'][0],
        'grant_type': 'authorization_code',
    }

    response = requests.post(token_url, data=token_data)
    token_info = response.json()

    if 'access_token' not in token_info:
        return 'Access denied: Unable to obtain access token.'

    session['gmail_token'] = (token_info['access_token'], '')
    user_info = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={'Authorization': f"Bearer {token_info['access_token']}"})
    user_info = user_info.json()

    return f"Logged in as: {user_info['email']}"

@app.route('/logout')
def logout():
    session.pop('gmail_token', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
