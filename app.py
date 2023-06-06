from flask import Flask
from flask import Flask, render_template, request,jsonify ,send_file
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
# Set the path to the certificate template image
CERTIFICATE_TEMPLATE_PATH = "certificate-template.jpg"

CERTIFICATE_TEMPLATE_FILE_PATH = "/static/certificate"

# Set the path to the text file containing names
NAMES_FILE_PATH = "static/public"

# Set the path where the generated certificates will be saved
CERTIFICATES_DIR = "static/output"

# Create the certificates directory if it doesn't already exist
os.makedirs(CERTIFICATES_DIR, exist_ok=True)



# Set the font parameters
#font_path = "/home/abc/Downloads/MaiyaRegular.ttf"
font_path = "/home/abc/Downloads/MangalRegular.ttf"
font_size = 50
font_color = (0, 0, 150)
font = ImageFont.truetype(font_path, font_size)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/path/to/upload/folder'

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        toggle_switch = request.form.get('toggle_switch')
        file_list = []
        if toggle_switch == 'on':
            print("toggle switch is On")
            try:
                #uploading template
                template = request.files['certificate_template']
                path = os.getcwd() + '/' + CERTIFICATE_TEMPLATE_FILE_PATH
                template_path = os.path.join(path, template.filename)
                template.save(template_path)
                #uploading certificate names
                file = request.files['file']
                path = os.getcwd() + '/' + NAMES_FILE_PATH
                file_path = os.path.join(path, file.filename)
                file.save(file_path)
                with open(file_path) as f:
                    names = [line.strip() for line in f]
                    for line in names:
                        certificate_path = certification_generate(line,template_path) 
                        file_list.append(certificate_path)                          
            except:
                raise
        else:
            # generate single certificate
            user_name = request.form['user_name'] if request.form['user_name'] else ""
            template = request.files['certificate_template']
            path = os.getcwd() + '/' + CERTIFICATE_TEMPLATE_FILE_PATH
            template_path = os.path.join(path, template.filename)
            template.save(template_path)
            certificate_path = certification_generate(user_name,template_path)
            file_list.append(certificate_path)
        return render_template("uploaded.html",content=file_list)      
        # Handle form submission   
    else:
        # Render the form
        return render_template('index.html')

def certification_generate(name,template_path):
    # Load the certificate template image
    certificate_template_image = cv2.imread(template_path)
    certificate_image = certificate_template_image.copy()
    # Create a PIL ImageDraw object to draw the name on the certificate image
    pil_image = Image.fromarray(cv2.cvtColor(certificate_image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)

    # Calculate the position of the name based on the font size and the size of the image
    text_bbox = draw.textbbox((0, 0), name, font=font)
    name_width, name_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    x = 659
    y = 395

    # Draw the name on the certificate image using the PIL ImageDraw object
    draw.text((x, y), name, font=font, fill=font_color)

    # Convert the PIL image back to a NumPy array and save the certificate image
    certificate_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    name_space = name.split(" ")
    name_space = "_".join(name_space)
    certificate_path = os.path.join(CERTIFICATES_DIR, f"{name_space}.jpg")
    cv2.imwrite(certificate_path, certificate_image)
    return certificate_path

 
@app.route('/certificate/<certificate_path>')
def display_certificate(certificate_path):
    return send_file(certificate_path, mimetype='image/jpg')

@app.route('/application_form', methods=['GET', 'POST'])
def application_form():
    print(f'request method {request.method}')
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        dob = request.form.get('dob')
        age = request.form.get('age')
        agree = request.form.get('agreeCheckbox')
        gender = request.form.get('gender')

        # Do something with the form data
        print(f'full Name of candidate is {first_name} {last_name} \n Contact No. {mobile} Email Addr {email} Birthdate: {dob} Gender : {gender} of age {age}')
        # ...

        # Return a response or redirect to another page
        return render_template('application_form2.html')
    return render_template('application_form.html') 

@app.route('/application_form11', methods=['GET', 'POST'])
def application_form11():
    print(f'request method {request.method}')
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        dob = request.form.get('dob')
        age = request.form.get('age')
        agree = request.form.get('agreeCheckbox')
        gender = request.form.get('gender')

        # Do something with the form data
        print(f'full Name of candidate is {first_name} {last_name} \n Contact No. {mobile} Email Addr {email} Birthdate: {dob} Gender : {gender} of age {age}')
        # ...

        # Return a response or redirect to another page
        return render_template('application_form2.html')
    return render_template('application_form.html') 

@app.route('/donation_form', methods=['GET', 'POST'])
def donation_form():
    return render_template('donation_form.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")