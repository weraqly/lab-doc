from datetime import datetime
from ..models import db
from ..models.entities import Booking, Room, Customer


class BookingService:
    @staticmethod
    def calculate_total_price(room, check_in, check_out):
        nights = (check_out - check_in).days
        if nights <= 0:
            raise ValueError('Дата виїзду має бути пізніше за дату заїзду.')

        base_price = room.price_per_night * nights
        breakfast_fee = 12 * nights if room.has_breakfast else 0
        peak_multiplier = 1.15 if check_in.month in (6, 7, 8, 12) else 1.0
        total = (base_price + breakfast_fee) * peak_multiplier
        return round(total, 2)

    @staticmethod
    def create_booking(customer_data, room_id, check_in, check_out):
        room = Room.query.get_or_404(room_id)
        if not room.is_available:
            raise ValueError('Номер вже недоступний.')

        customer = Customer.query.filter_by(email=customer_data['email']).first()
        if customer is None:
            customer = Customer(**customer_data)
            db.session.add(customer)
            db.session.flush()

        total_price = BookingService.calculate_total_price(room, check_in, check_out)

        room.is_available = False
        booking = Booking(
            customer_id=customer.id,
            room_id=room.id,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            booking_status='Reserved',
            payment_hold_status='Funds blocked'
        )
        db.session.add(booking)
        db.session.commit()
        return booking

    @staticmethod
    def release_room(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        booking.booking_status = 'Cancelled'
        booking.payment_hold_status = 'Released'
        booking.room.is_available = True
        db.session.commit()
        return booking

    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()
