from ..models import db
from ..models.entities import HotelChain, Hotel, Room, Review


class HotelService:
    @staticmethod
    def get_dashboard_data():
        return {
            'chains_count': HotelChain.query.count(),
            'hotels_count': Hotel.query.count(),
            'rooms_count': Room.query.count(),
            'reviews_count': Review.query.count(),
            'available_rooms_count': Room.query.filter_by(is_available=True).count(),
        }

    @staticmethod
    def average_rating(hotel):
        if not hotel.reviews:
            return 0
        return round(sum(r.rating for r in hotel.reviews) / len(hotel.reviews), 2)

    @staticmethod
    def create_chain(data):
        chain = HotelChain(**data)
        db.session.add(chain)
        db.session.commit()
        return chain

    @staticmethod
    def create_hotel(data):
        hotel = Hotel(**data)
        db.session.add(hotel)
        db.session.commit()
        return hotel

    @staticmethod
    def create_room(data):
        room = Room(**data)
        db.session.add(room)
        db.session.commit()
        return room
