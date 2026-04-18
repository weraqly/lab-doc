from flask import Blueprint, render_template, request, redirect, url_for
from ..models import db
from ..models.entities import Room, Hotel
from ..services.hotel_service import HotelService

room_bp = Blueprint('rooms', __name__)


@room_bp.route('/')
def list_rooms():
    rooms = Room.query.order_by(Room.hotel_id, Room.room_number).all()
    return render_template('rooms/list.html', rooms=rooms)


@room_bp.route('/create', methods=['GET', 'POST'])
def create_room():
    hotels = Hotel.query.order_by(Hotel.name).all()
    if request.method == 'POST':
        HotelService.create_room({
            'hotel_id': int(request.form['hotel_id']),
            'room_number': request.form['room_number'],
            'room_type': request.form['room_type'],
            'capacity': int(request.form['capacity']),
            'price_per_night': float(request.form['price_per_night']),
            'is_available': 'is_available' in request.form,
            'has_breakfast': 'has_breakfast' in request.form,
        })
        return redirect(url_for('rooms.list_rooms'))
    return render_template('rooms/form.html', room=None, hotels=hotels)


@room_bp.route('/<int:room_id>/edit', methods=['GET', 'POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    hotels = Hotel.query.order_by(Hotel.name).all()
    if request.method == 'POST':
        room.hotel_id = int(request.form['hotel_id'])
        room.room_number = request.form['room_number']
        room.room_type = request.form['room_type']
        room.capacity = int(request.form['capacity'])
        room.price_per_night = float(request.form['price_per_night'])
        room.is_available = 'is_available' in request.form
        room.has_breakfast = 'has_breakfast' in request.form
        db.session.commit()
        return redirect(url_for('rooms.list_rooms'))
    return render_template('rooms/form.html', room=room, hotels=hotels)


@room_bp.route('/<int:room_id>/delete', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('rooms.list_rooms'))
