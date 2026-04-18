from flask import Flask
from .models import db
from .seed import seed_data


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking_platform.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'booking-demo-secret'

    db.init_app(app)

    with app.app_context():
        from .models.entities import HotelChain, Hotel, Room, Review, Booking, Customer
        db.create_all()
        seed_data()

    from .controllers.main_controller import main_bp
    from .controllers.chain_controller import chain_bp
    from .controllers.hotel_controller import hotel_bp
    from .controllers.room_controller import room_bp
    from .controllers.review_controller import review_bp
    from .controllers.booking_controller import booking_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chain_bp, url_prefix='/chains')
    app.register_blueprint(hotel_bp, url_prefix='/hotels')
    app.register_blueprint(room_bp, url_prefix='/rooms')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(booking_bp, url_prefix='/bookings')

    return app
