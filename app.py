from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'image_editor/uploads'
ALLOWED_EXTENSIONS = {'avif', 'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = "qwe\\rt\\yuiopas\\dfghjkl\\\zxc\\vbnm"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def img_process(filename, operation):
    print("filname is", filename, "operation name is", operation)
    img = cv2.imread(f"image_editor/uploads/{filename}")
    match operation:
        case "greyscale":
            new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newfilename = f"image_editor/static/{filename}"
            res = f"static/{filename}"
            cv2.imwrite(newfilename, new_img)
            return res
        case "jpeg":
            newfilename = f"image_editor/static/{filename.split('.')[0]}.jpeg"
            res = f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newfilename, img)
            return res
        case "jpg":
            newfilename = f"image_editor/static/{filename.split('.')[0]}.jpg"
            res = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename, img)
            return res
        case "webp":
            newfilename = f"image_editor/static/{filename.split('.')[0]}.webp"
            res = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename, img)
            return res
        case "png":
            newfilename = f"image_editor/static/{filename.split('.')[0]}.png"
            res = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img)
            return res
    pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods = ["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = img_process(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target = '_blank'>Here</a>")
            return render_template("index.html")

        


app.run(debug=True, port=5001)