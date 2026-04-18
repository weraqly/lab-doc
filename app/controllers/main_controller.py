from flask import Blueprint, render_template
from ..services.hotel_service import HotelService
from ..models.entities import Hotel, Room, Booking

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    stats = HotelService.get_dashboard_data()
    recent_hotels = Hotel.query.order_by(Hotel.id.desc()).limit(5).all()
    available_rooms = Room.query.filter_by(is_available=True).limit(5).all()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    return render_template('index.html', stats=stats, recent_hotels=recent_hotels, available_rooms=available_rooms, recent_bookings=recent_bookings, hotel_service=HotelService)
