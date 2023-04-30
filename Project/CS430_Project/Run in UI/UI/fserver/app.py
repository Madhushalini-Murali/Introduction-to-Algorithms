from flask import Flask , send_file
from flask import request
from flask_cors import CORS
import subprocess
from pathlib import Path



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
@app.route('/api/endpoint', methods=['POST'])
def show_data():
    global data
    data = request.get_json()
    print(data)
    testapc()
    return "successful"

@app.route('/getFileContent')
def get_file_content():
    # file_path = 'C:/uploads/myFile.txt'
    file_path = 'C:/Users/vaish/Documents/UI/fserver/output.txt'
    return send_file(file_path)

def testapc():
    # arg1 = 'value1'
    # arg2 = 'value2'
    # arg3 = 'value3'
    path_val = Path().absolute();
    subprocess.call(['python', 'Project_Algo.py', data["message1"], data["message2"], data["message3"],path_val ])
    # print(data["message1"])
    print("Directory Path:", Path().absolute())
    return "Testapc_succes"



if __name__ == '__main__':
    app.run(debug = True)
