from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.entities import Booking, Room
from ..services.booking_service import BookingService

booking_bp = Blueprint('bookings', __name__)


@booking_bp.route('/')
def list_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('bookings/list.html', bookings=bookings)


@booking_bp.route('/create', methods=['GET', 'POST'])
def create_booking():
    rooms = Room.query.order_by(Room.hotel_id, Room.room_number).all()
    error = None
    preview_total = None

    if request.method == 'POST':
        try:
            room_id = int(request.form['room_id'])
            check_in = BookingService.parse_date(request.form['check_in'])
            check_out = BookingService.parse_date(request.form['check_out'])

            customer_data = {
                'full_name': request.form['full_name'],
                'email': request.form['email'],
                'phone': request.form['phone'],
                'loyalty_level': request.form['loyalty_level'],
            }

            if 'preview' in request.form:
                room = Room.query.get_or_404(room_id)
                preview_total = BookingService.calculate_total_price(room, check_in, check_out)
            else:
                BookingService.create_booking(customer_data, room_id, check_in, check_out)
                flash('Бронювання успішно створене, кошти заблоковано.', 'success')
                return redirect(url_for('bookings.list_bookings'))
        except Exception as ex:
            error = str(ex)

    return render_template('bookings/form.html', rooms=rooms, error=error, preview_total=preview_total)


@booking_bp.route('/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    BookingService.release_room(booking_id)
    flash('Бронювання скасовано, блокування коштів знято.', 'info')
    return redirect(url_for('bookings.list_bookings'))
