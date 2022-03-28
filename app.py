from re import DEBUG, sub
from flask import Flask, request,render_template,request
from matplotlib.pyplot import ion
from werkzeug.utils import secure_filename
import os
import subprocess
import glob
from flask_cors import CORS
import mysql.connector 

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect (
    host="ccc-mysqlserver.mysql.database.azure.com",
    user="chayanis@ccc-mysqlserver",
    password="1q2w3e4r@kku",
    database="ccc_database",
    port=3306,
    ssl_ca=('BaltimoreCyberTrustRoot.crt.pem')
)


mycursor = db.cursor()

uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return
    id = request.form.get("id")
    print(id)
    siteId = request.form.get("siteId")
    print(siteId)
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
        #subprocess.run("ls")
    subprocess.run(['python', 'detect.py','--weight','best.pt', '--source', os.path.join(uploads_dir, secure_filename(video.filename)),'--save-txt'],shell=True)
        #return os.path.join(uploads_dir, secure_filename(video.filename))
    subprocess.run(['python', 'detect_worker.py','--weight','best_worker.pt', '--source', os.path.join(uploads_dir, secure_filename(video.filename)),'--save-txt'],shell=True)
    obj = secure_filename(video.filename)
    
    list_of_files = glob.glob('./static/labels/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
   
    file = open(latest_file, "r")
    line_count_hardhat = 0
    line_count_no_hardhat = 0
    
    for line in file:
        if line != "\n":
            firt_label = line[0]
            if firt_label == "0":
                line_count_no_hardhat += 1
            elif firt_label == "1":
                line_count_hardhat += 1
            else:
                line_count_hardhat = 0
                line_count_no_hardhat = 0
    
    list_of_files_worker= glob.glob('./static/static-worker/labels/*') # * means all if need specific format then *.csv
    latest_file_worker = max(list_of_files_worker, key=os.path.getctime)
    print(latest_file_worker)
   
    file = open(latest_file_worker, "r")
    line_count_person = 0
    
    for line in file:
        if line != "\n":
            firt_label = line[0]
            if firt_label == "0":
                line_count_person += 1
            elif firt_label == "1":
                line_count_person += 1
            else:
                line_count_person = 0

    file.close()
    mycursor = db.cursor()
    mycursor.execute("""INSERT INTO lab (id_lab,id_mng_lab,id_site_lab,id_result_person,name_result_person,result_person,id_result_hardhat,name_result_hardhat,result_hardhat,id_result_nohardhat,name_result_nohardhat,result_nohardhat, date_lab, time_lab)
    VALUES (NULL,%s, %s,%s,(select Name_result as name_result_person from class_result where Id_result = %s) , %s,%s,(select Name_result as name_result_hardhat from class_result where Id_result = %s) ,%s,%s,(select Name_result as name_result_nohardhat from class_result where Id_result = %s) ,%s, SYSDATE(),time(NOW()))""",
    (id,siteId,1,1,line_count_person,2,2,line_count_hardhat,3,3,line_count_no_hardhat))
    db.commit()
    mycursor.close()
    print(line_count_person)
    print(line_count_hardhat)
    print(line_count_no_hardhat)
   
    return obj
