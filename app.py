import os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,redirect,url_for
import numpy as np
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
# importing all the necessary libraries for code implementation

app=Flask(__name__)

model = load_model('vgg19.h5') # loading the saved deep learning model into the variable model 
image_size = 224
def model_predict(img_path): # this function is to load the given image and convert it into numerical array format comes under preprocessing image and passing this to model for prediction
    img=image.load_img("static/uploads/"+img_path,target_size=(image_size,image_size))
    x = image.img_to_array(img) # here
    x/=255.0
    x = np.expand_dims(x,axis=0)
    img_data = x
    a = model.predict(img_data)
    return a
# predicted value will be returned by the model  

@app.route('/') # by default the home page will be displayed when the server created on local host.
def accessthesite():
    return render_template('index.html') # used to display the index.html page 
@app.route('/home')  # used to display the index.html page when we click on home button on website
def home():
    return render_template('index.html')
@app.route('/contact') # used to display the contact.html page when we click on contact button on website
def contactpage():
    return render_template('contact.html')
@app.route('/about') # used to display the about.html page when we click on about button on website
def aboutpage():
    return render_template('about.html')
@app.route('/test') # used to display the service.html page when we click on test button on website
def testpage():
    return render_template('service.html')

@app.route('/predict',methods=['POST','GET']) # the posted request from the service.html page when we upload image and click submit is received over here
def predict():
    # Check if the 'imagefile' key is present in the files part of the request
    if 'imagefile' not in request.files:  # If 'imagefile' is not in request files, redirect back to the URL of the request
        return redirect(request.url)
    file=request.files['imagefile'] # put this imagefile into the file
    if file.filename == '':     # Check if the file has a name
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)  # Securing the filename to avoid any security issues with file names
        upload_folder = 'static/uploads'         # defining the upload folder where this file will be saved
        if not os.path.exists(upload_folder):         # Check if the upload folder already exists, if not then create it
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, filename)         # Craete the full path where the file will be saved
        file.save(file_path)

        preds = model_predict(filename)[0][0] # passed file to model_predict function
        if(preds>=0.90):
            predictn = "Eye is having Cataract"
        else:
            predictn = "Eye is Normal"
        return render_template('service.html', predictn=predictn) # returning the result obtained to the service.html page 
if __name__ == '__main__':
    app.run(debug=True)


























# from flask import Flask,render_template,request
# import pickle
# import numpy as np
# from tensorflow.keras.preprocessing.image import load_img,img_to_array
# app=Flask(__name__)

# # model = pickle.load(open('cat_model.pkl','rb'))
# @app.route('/')
# def accessthesite():
#     return render_template('index.html')
# @app.route('/home')
# def home():
#     return render_template('index.html')
# @app.route('/contact')
# def contactpage():
#     return render_template('contact.html')
# @app.route('/about')
# def aboutpage():
#     return render_template('about.html')
# @app.route('/test')
# def testpage():
#     return render_template('service.html')
    
# @app.route("/predict"   ,methods=['POST','GET'])
# def predict():
#     imagefile = request.files['imagefile']
#     imagefile.save("imagefile.png")
#     return "welcome to cataract prediction"
# if __name__ == '__main__':
#     app.run(debug=True)

# from tensorflow.keras.preprocessing.image import load_img,img_to_array
# def preprocess_external_image(image_path, image_size):
#     image = load_img(image_path, target_size=(image_size, image_size))
#     image = img_to_array(image)
#     image = image / 255.0
#     image = np.expand_dims(image, axis=0)
#     return image
# external_image_path = "/content/3507_left.jpg"
# preprocessed_image = preprocess_external_image(external_image_path, image_size)
# prediction = model.predict(preprocessed_image)
# if prediction > 0.5:
#     print("image shows signs of Cataract.")
# else:
#     print("image is Normal.")
