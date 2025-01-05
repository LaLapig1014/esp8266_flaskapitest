from flask import Flask, request, render_template
from flask import Flask, send_from_directory
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import base64
import json

def get_firebase_credential():
    with open('esp8266_encrypt.txt', 'r', encoding="UTF-8") as enc:
        encryptdata=enc.read()
    #print(encryptdata)
    decoded_bytes = base64.b64decode(encryptdata)
    decoded_data = json.loads(decoded_bytes.decode('utf-8'))  # 解碼後重新轉換為 JSON
    #print("\nDecoded Data:")
    #print(decoded_data)
    return decoded_data
    # 返回密鑰資訊（原來 JSON 檔案的內容）
    
cred = credentials.Certificate(get_firebase_credential())  # 替換為你的密鑰路徑
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://esp8266-apitest-default-rtdb.asia-southeast1.firebasedatabase.app/'  # 替換為你的 Realtime Database URL
})



def get_data_from_realtime_db():
    ref = db.reference('ESP8266')  # 替換為你需要讀取的節點名稱
    data = ref.get()
    print(data)
    return data
def update_data_in_realtime_db(ID,status):
    ref = db.reference('ESP8266')  # 替換為你需要更新的節點名稱
    new_data = {
        "ID": ID,
        "status": status
    }
    ref.set(new_data)  # 完全覆蓋該節點的資料
    print("Data updated successfully!")

def getpin():
    pin=""
    for i in range(6):
        pin+=str(random.randint(0,9))
    return pin

app = Flask(__name__)
@app.route("/")
def index():
    msg=""
    D=get_data_from_realtime_db()
    msg=D["ID"]+","+D["status"]
    
    print(msg)
    return render_template("index.html",msg=msg)
@app.route("/hello")
def yanwei():
    return "Hello"


@app.route("/getdata",methods=["GET"])
def getdata():

    D=get_data_from_realtime_db()
    
    return jsonify(D)

@app.route("/putdatajson",methods=["PUT"])
def putdatajson():
    if request.is_json:
        data = request.get_json() 
        MID=data.get("MID")
        status = data.get('status')
        print(MID,status)
        return jsonify({"message": f"Received data: ID={MID}, status={status}"}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
@app.route("/putdataurl",methods=["GET","PUT"])
def putdataurl():
    params = request.args.to_dict()
    print(params)
    MID=params["MID"]
    status=params["status"]

    update_data_in_realtime_db(MID,status)

    #--
    
    #--
    return jsonify({"message": f"Received data:MID:{MID},status:{status}"}), 200
    #http://192.168.38.100:8080/putdataurl?MID=A03&status=HIHI
@app.route("/test",methods=["GET"])
def test():

    return jsonify({"message": "Hello from Flask!"})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
    #app.run(debug=True)


#render_template將會找尋html檔案傳送給使用者