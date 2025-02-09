from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Route to fetch eBay images
@app.route('/fetch_ebay', methods=['POST'])
def fetch_ebay():
    category = request.json.get('category')
    # Call your eBay fetching script (e.g., App/ebay/main.py)
    subprocess.run(['python3', 'App/ebay/main.py', category])
    return jsonify({"status": "success", "message": "Images fetched and saved."})

# Route to run YOLO sorting
@app.route('/run_yolo', methods=['POST'])
def run_yolo():
    # Call your YOLO sorting script (e.g., App/yolo/main.py)
    subprocess.run(['python3', 'App/yolo/main.py'])
    return jsonify({"status": "success", "message": "Images sorted."})

# Route to get sorted images for display
@app.route('/get_images', methods=['GET'])
def get_images():
    image_folder = 'App/static/images/with_tabs'  # Change to 'without_tabs' if needed
    images = os.listdir(image_folder)
    image_data = []
    for img in images:
        item_number = img.split('.')[0]  # Extract eBay item number from filename
        ebay_link = f"https://www.ebay.com/itm/{item_number}"
        image_data.append({"filename": img, "link": ebay_link})
    return jsonify(image_data)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
