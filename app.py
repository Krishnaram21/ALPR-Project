from flask import Flask, render_template, request
import easyocr

app = Flask(__name__)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/detect')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['image']

    if file.filename == '':
        return render_template('index.html', error='No Selected File.')

    if file:
        image = file.read()
        extracted_text = extract_text(image)
        return render_template('index.html', text=extracted_text, filename=file.filename, image_data=image)

def extract_text(image):
    result = reader.readtext(image)
    extracted_text = '\n'.join([text[1] for text in result])
    return extracted_text

if __name__ == '__main__':
    app.run(debug=True)
