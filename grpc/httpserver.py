from flask import Flask, current_app
app = Flask(__name__)

@app.route('/g/<input_text>', methods=['GET', 'POST'])
def word_cloud_running(input_text):
    return input_text + 'dd'

with app.app_context():
     print(current_app.name)
app.run(debug=False, host='0.0.0.0', port=3106, threaded=False)

