from flask import Blueprint, render_template, request, redirect, url_for
from ..models import db
from ..models.entities import Hotel, HotelChain
from ..services.hotel_service import HotelService

hotel_bp = Blueprint('hotels', __name__)


@hotel_bp.route('/')
def list_hotels():
    hotels = Hotel.query.order_by(Hotel.name).all()
    return render_template('hotels/list.html', hotels=hotels, hotel_service=HotelService)


@hotel_bp.route('/create', methods=['GET', 'POST'])
def create_hotel():
    chains = HotelChain.query.order_by(HotelChain.name).all()
    if request.method == 'POST':
        HotelService.create_hotel({
            'chain_id': int(request.form['chain_id']),
            'name': request.form['name'],
            'city': request.form['city'],
            'country': request.form['country'],
            'address': request.form['address'],
            'stars': int(request.form['stars']),
            'latitude': float(request.form['latitude']) if request.form['latitude'] else None,
            'longitude': float(request.form['longitude']) if request.form['longitude'] else None,
            'description': request.form['description'],
        })
        return redirect(url_for('hotels.list_hotels'))
    return render_template('hotels/form.html', hotel=None, chains=chains)


@hotel_bp.route('/<int:hotel_id>/edit', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    chains = HotelChain.query.order_by(HotelChain.name).all()
    if request.method == 'POST':
        hotel.chain_id = int(request.form['chain_id'])
        hotel.name = request.form['name']
        hotel.city = request.form['city']
        hotel.country = request.form['country']
        hotel.address = request.form['address']
        hotel.stars = int(request.form['stars'])
        hotel.latitude = float(request.form['latitude']) if request.form['latitude'] else None
        hotel.longitude = float(request.form['longitude']) if request.form['longitude'] else None
        hotel.description = request.form['description']
        db.session.commit()
        return redirect(url_for('hotels.list_hotels'))
    return render_template('hotels/form.html', hotel=hotel, chains=chains)


@hotel_bp.route('/<int:hotel_id>/delete', methods=['POST'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    return redirect(url_for('hotels.list_hotels'))
