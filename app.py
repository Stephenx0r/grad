from datetime import datetime
from flask import Flask, send_file, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import qrcode
import logging
import uuid
import os

# Initialize Flask app
app = Flask(__name__)
# Configure SQLAlchemy with SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qr_scans.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize SQLAlchemy with app
db = SQLAlchemy(app)

# A directory to store the QR code images if it doesn't exist
QR_IMAGES_FOLDER = 'static/qr_codes'
if not os.path.exists(QR_IMAGES_FOLDER):
    os.makedirs(QR_IMAGES_FOLDER)

# Define QRScan model
class QRScan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.String(120), unique=True, nullable=False)
    scan_count = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'<QRScan {self.qr_id}>'

# Function to generate QR code
def generate_qr(data, qr_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join(QR_IMAGES_FOLDER, f"{qr_id}.png")
    img.save(img_path)
    return img_path

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate QR code
@app.route('/qr', methods=['GET'])
def qr_code():
    # Hardcoded IP address
    ip_address = "193.0.0.102"

    # A unique ID for each QR code
    qr_id = str(uuid.uuid4())
    data = f"http://{ip_address}:5000/scan/{qr_id}"
    app.logger.info('Generating QR code with data: ' + data)
    img_path = generate_qr(data, qr_id)
    app.logger.info('QR code generated successfully.')

    # New QR code entry to the database
    new_qr = QRScan(qr_id=qr_id)
    db.session.add(new_qr)
    db.session.commit()

    return send_file(img_path, mimetype='image/png')

# Route to scan QR code
@app.route('/scan/<qr_id>', methods=['GET'])
def scan(qr_id):
    qr_scan = QRScan.query.filter_by(qr_id=qr_id).first()
    if not qr_scan:
        app.logger.warning(f'Scan attempt for non-existent QR code: {qr_id}')
        abort(404, description="QR code not found.")

    if qr_scan.scan_count >= 2:
        app.logger.info(f'Access denied for QR code: {qr_id} - Maximum scan limit reached.')
        return render_template('access_denied.html'), 403
    else:
        current_time = datetime.utcnow()
        if qr_scan.scan_count == 0:
            qr_scan.first_scan_time = current_time
        elif qr_scan.scan_count == 1:
            qr_scan.second_scan_time = current_time
        qr_scan.scan_count += 1
        db.session.commit()
        app.logger.info(f'QR code {qr_id} scanned successfully. Scan count: {qr_scan.scan_count}')
        return render_template('access_granted.html')

# Main entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if not os.path.exists('qr_scans.db'):
        with app.app_context():
            db.create_all()
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)  # Bind to all interfaces