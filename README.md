# QR Scan Flask App

This is a Flask application that creates, saves and scans QR codes. It uses the SQLAlchemy library for interacting with an SQLite database to store QR code scan data and utilizes the qrcode library for generating QR code images.

## Project Overview 

The application is capable of the following:

- Generate a new QR code with a unique URL attached to it.
- Scan the generated QR code by accessing the URL in the QR code.
- Limit the number of times a QR code can be scanned.
- Log all activities in the application.

The project main modules are:

1. **Flask Application Configuration** - Includes setup for SQLAlchemy and QR code images folder.
2. **QRScan Model** - The database model for storing each QR code's details.
3. **Routes** 
   - `/` Home Route
   - `/qr` Generate QR code
   - `/scan/< qr_id >` Scan QR code
4. **QR Generation** - Function to generate QR code image files.
   
## Installation & Usage

### Installation

To run the application in your local environment:

1. Clone the repository.
2. Install the required packages.
3. Run the app.

### Usage

Access `localhost:5000` on your browser to see the application in action. The `/qr` route will generate a new QR code each time it is accessed. The QR code can be scanned twice before it becomes inaccessible via the `/scan` route.

## Project Status and Future Enhancements

While this app serves as a great starting point for managing and interacting with QR codes using Flask, please note that it is a basic model and would require more functionalities and robust features to be used as a real-world application. 
