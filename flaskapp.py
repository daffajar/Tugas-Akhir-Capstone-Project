from flask import Flask, render_template, Response,jsonify,request,session,redirect,url_for
from flask_wtf import FlaskForm
from db_config import app
from wtforms import FileField, SubmitField,StringField,DecimalRangeField,IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import subprocess
import os
import pandas
import cv2
import datetime
import json
from YOLO_Video import video_detection,update_webcam_db,web_detection


 


class UploadFileForm(FlaskForm):
    
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Run")


def generate_frames(path_x = ''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
    

def generate_frames_web(path_x):
    yolo_output = web_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        

@app.route('/', methods=['GET','POST'])

@app.route('/home', methods=['GET','POST'])
def home():
    session.clear()
    return redirect(url_for("refresh"))


@app.route("/webcam/start", methods=['GET','POST'])
def webcam():
    session.clear()
    return render_template('webcam.html')


@app.route("/webcam/stop", methods=['GET','POST'])
def webcam_stop():
    session.clear()
    rows = pandas.read_json("webcam_db.json")
    table = rows["detections"]
    return render_template('webcam_stop.html',table=table)


@app.route("/webcam/reset", methods=['GET','POST'])
def delete_webcam_data():
    # Clear session
    session.clear()

    # Delete the contents of webcam_db.json
    if os.path.exists("webcam_db.json"):
        with open("webcam_db.json", "r") as file:
            data = json.load(file)
        if "detections" in data:
            data["detections"]=[]
        with open("webcam_db.json", "w") as file:
            json.dump(data, file)
    return redirect('/webcam/stop')


@app.route("/video/reset", methods=['GET','POST'])
def delete_video_data():
    # Clear session
    session.clear()

    # Delete the contents of db.json
    if os.path.exists("db.json"):
        with open("db.json", "r") as file:
            data = json.load(file)
        if "detections" in data:
            data["detections"]=[]
        with open("db.json", "w") as file:
            json.dump(data, file)
    return redirect('/video/upload')


@app.route('/video/detect', methods=['POST'])
def front():
    
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename))) 
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))  
    return render_template('video_detect.html', form=form)



@app.route("/webcam/update", methods=['GET'])

def update():
    with open("webcam_db.json",'r+') as file:
        
        file_data = json.load(file)


        cur = len(file_data["detections"]) - 1 if len(file_data["detections"]) > 0 else 0
        file_data["detections"][cur]["end"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        
        file.seek(0)

        json.dump(file_data, file, indent = 4)

        file.close()
    
    session.clear()
    return redirect("/webcam/stop")


@app.route("/video/upload", methods=['GET'])

def refresh():
    session.clear()
    form = UploadFileForm()

    rows = pandas.read_json("db.json")
    table = rows["detections"]
    
    return render_template('video_upload.html',form=form,table=table)
            
@app.route('/video')
def video():
    return Response(generate_frames(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webapp')

def webapp():

    return Response(generate_frames_web(path_x=1), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)