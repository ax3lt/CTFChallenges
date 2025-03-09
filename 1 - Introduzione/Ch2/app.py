from flask import Flask, request, render_template_string

app = Flask(__name__)

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Form Submission with JSON response</title>
</head>
<body>
    <h1>Submit Your Data</h1>
    <form method="POST">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email"><br><br>
        <input type="submit" value="Submit">
    </form>

    <p>Codice python equivalente all'invio del form ma ricezione di una risposta JSON:</p>
    <pre>
        import requests
        url = 'http://localhost:8080/'
        data = {'name': 'John Doe', 'email': 'valid@email.it'}
        response = requests.post(url, data=data)
        print("Nome:", response.json()['name'])
        print("Email:", response.json()['email'])
    </pre>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        return {'name': name, 'email': email}
    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=False)