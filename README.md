# CloudSentinel MarketLink

CloudSentinel MarketLink is a web-based digital marketplace project developed under CloudSentinel Technologies. It is designed to connect buyers, sellers, SMEs, service providers, students, farmers, and local businesses across Nigeria.

The platform allows users to register, login, post product or service listings, upload images, search listings, filter by category, select Nigerian states and LGAs, manage seller dashboards, mark products as sold, and communicate through a real-time chat system.

## Project Purpose

CloudSentinel MarketLink serves as a digital bridge between businesses and customers. The goal is to support SME digitalization, local commerce, and safe online-to-offline trading.

This project is part of CloudSentinel Technologies’ portfolio of digital solutions and can be upgraded into a real operational marketplace.

## Key Features

- User registration and login
- Seller dashboard
- Product and service listing
- Image upload with maximum size of 1MB
- Search and category browsing
- Nigerian states and LGA selection
- Product detail page
- Safe trading warning
- Mark listing as sold
- Delete listing
- Edit listing
- Real-time buyer and seller chat
- Inbox page for conversations
- Mobile responsive marketplace interface

## Safety Notice

CloudSentinel MarketLink encourages safe trading.

Users should not send money in advance unless they personally trust the seller. Buyers and sellers are advised to meet in a public market, shop, office, or secure physical location and inspect products before payment.

## Technology Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO

### Frontend
- HTML
- CSS
- JavaScript
- Jinja2 Templates

### Database
- SQLite for local development
- PostgreSQL recommended for deployment

### Other Tools
- Pillow for image validation
- Gunicorn for deployment
- Gevent WebSocket worker for real-time chat hosting

## Project Structure

cloudsentinel-marketlink/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── README.md
├── routes/
├── services/
├── data/
├── templates/
├── static/
└── instance/

## Deployment

The project can be deployed on:

Railway
Render

Recommended production start command:

gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app

## Image Upload Rule

Uploaded product images must be:

JPG, JPEG, or PNG
Maximum size: 1MB

## Future Improvements

Admin dashboard
Seller verification badge
Report suspicious listing
Listing approval system
Product boosting
Escrow payment concept
AI scam detection
Advanced search and filters
Push notifications
Mobile app version

## Author

Muhammad Yuguda
Founder, CloudSentinel Technologies
Cybersecurity • Compliance • Digital Solutions

## License

This project is developed for educational, portfolio, and startup demonstration purposes.