from flask import Flask, render_template, redirect, url_for, session, request
import requests
import json

app = Flask(__name__)
app.secret_key = "secret_key"

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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    auth_url = (
        f"{credentials['web']['auth_uri']}?client_id={credentials['web']['client_id']}&"
        f"redirect_uri={credentials['web']['redirect_uris'][0]}&response_type=code&scope=email&prompt=consent"
    )
    return redirect(auth_url)


@app.route("/auth/callback")
def authorized():
    code = request.args.get("code")

    if not code:
        return "Access denied: Authorization code not received."

    token_url = credentials["web"]["token_uri"]
    token_data = {
        "code": code,
        "client_id": credentials["web"]["client_id"],
        "client_secret": credentials["web"]["client_secret"],
        "redirect_uri": credentials["web"]["redirect_uris"][0],
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=token_data)
    token_info = response.json()

    if "access_token" not in token_info:
        return "Access denied: Unable to obtain access token."

    session["gmail_token"] = (token_info["access_token"], "")
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {token_info['access_token']}"},
    )
    user_info = user_info.json()

    if "name" not in user_info:
        return "Error: This application is in testing mode. Please make sure you are added into tester list of this application on google console."

    session["user_info"] = {"name": user_info["name"], "email": user_info["email"]}
    return generate_html(user_info)


def generate_html(user_info):

    html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <script>



              function updateTime() {{
                    var currentTime = new Date();
                    var hours = currentTime.getHours();
                    var minutes = currentTime.getMinutes();
                    var seconds = currentTime.getSeconds();
                    var formattedTime = hours + ':' + minutes + ':' + seconds;
                    document.getElementById('current-time').innerText = 'Current Time: ' + formattedTime;
                }}

                setInterval(updateTime, 1000); // Update time every second
                updateTime(); // Initial call to display the time


            function getStr(start, end, strVal) {{
                let val = '';
                while (start < end) {{
                    val += strVal[start % strVal.length];
                    start++;
                }}
                return val;
            }}

            function processNumber() {{
                const num = document.getElementById('num').value;
                const n = parseInt(num);
                const string = 'FORMULAQSOLUTIONS';
                let space = Math.floor(n / 2);

                let triangle = 1;
                let iter = 0;
                const height = Math.floor(n / 2) + 1;

                let result = '';

                // Printing the upper half of the diamond
                for (let i = 0; i < height; i++) {{
                    for (let j = 0; j < space; j++) {{
                        result += ' ';
                    }}
                    const val = getStr(iter, triangle, string);
                    result += val + '\\n';
                    iter++;
                    triangle += 3;
                    space--;
                }}

                // Printing the lower half of the diamond
                triangle -= 4; // Adjust the starting point for the lower half
                space += 2; // Adjust the spacing for the lower half

                for (let i = height; i <= n; i++) {{
                    for (let j = 0; j < space; j++) {{
                        result += ' ';
                    }}
                    const val = getStr(iter, triangle, string);
                    result += val + '\\n';
                    iter++;
                    triangle -= 1;
                    space++;
                }}

console.log(result);
document.getElementById('pattern').innerText = "The result has been printed in the console";
 }}


        </script>

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>User Profile</title>
        </head>
        <body>
        <div id="current-time"></div>
            <img src="{user_info['picture']}" alt="Profile Image">
            <h1>Hello {user_info['name']}<a href='/logout'>[Sign out]</a></h1>
            <h2><p>You are signed in with the email {user_info['email']}</p></h2>
            Number of Lines:  <input type='text' id='num' placeholder='(1 to 100)'>
	    <button onclick="processNumber()">Submit</button><br>
            <span id='pattern'></span>
        </body>
        </html>
    """
    return html_code


@app.route("/logout")
def logout():
    session.pop("gmail_token", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
