from flask import Flask, request, render_template
from flask import Flask, send_from_directory
from flask import Flask, jsonify
import json
def getpin():
    pin=""
    for i in range(6):
        pin+=str(random.randint(0,9))
    return pin

app = Flask(__name__)
@app.route("/")
def index():
    msg=""
    with open('data.json', 'r') as file:
        datas = json.load(file)
    M=datas["ESP8266"][0]
    msg=M["ID"]+","+M["state"]
    
    print(msg)
    return render_template("index.html",msg=msg)
@app.route("/hello")
def yanwei():
    return "Hello"


@app.route("/getdata",methods=["GET"])
def getdata():
    with open('data.json', 'r') as file:
        datas = json.load(file)
    D=datas["ESP8266"][0]
    return jsonify(D)

@app.route("/putdatajson",methods=["PUT"])
def putdatajson():
    if request.is_json:
        data = request.get_json() 
        MID=data.get("MID")
        state = data.get('state')
        print(MID,state)
        return jsonify({"message": f"Received data: ID={MID}, state={state}"}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
@app.route("/putdataurl",methods=["GET","PUT"])
def putdataurl():
    params = request.args.to_dict()
    print(params)
    MID=params["MID"]
    state=params["state"]
    #--
    with open('./data.json','r+',encoding="UTF-8") as jsonf:
            data=json.load(jsonf)
            for it in data["ESP8266"]:
                it["ID"]=MID
                it["state"]=state
                jsonf.seek(0)  # 將指標移回文件開頭
                json.dump(data, jsonf, ensure_ascii=False, indent=4) 
                jsonf.truncate()
    #--
    return jsonify({"message": f"Received data:MID:{MID},state:{state}"}), 200
    #http://192.168.38.100:8080/putdataurl?MID=A03&state=HIHI
@app.route("/test",methods=["GET"])
def test():

    return jsonify({"message": "Hello from Flask!"})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    #app.run(host="local", port=8080, debug=True)
    app.run(debug=True)


#render_template將會找尋html檔案傳送給使用者