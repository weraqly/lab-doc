from .models import db
from .models.entities import HotelChain, Hotel, Room, Customer, Review


def seed_data():
    if HotelChain.query.count() > 0:
        return

    chain1 = HotelChain(name='Skyline Stays', api_provider='Skyline API', integration_status='Connected', country='Spain')
    chain2 = HotelChain(name='Nordic Escape Group', api_provider='NordicBridge API', integration_status='Sandbox', country='Norway')
    db.session.add_all([chain1, chain2])
    db.session.flush()

    hotel1 = Hotel(chain_id=chain1.id, name='Skyline Barcelona Central', city='Barcelona', country='Spain', address='Avinguda Central 12', stars=4, latitude=41.38, longitude=2.17, description='Сучасний міський готель поруч із центром.')
    hotel2 = Hotel(chain_id=chain1.id, name='Skyline Costa Brava Resort', city='Girona', country='Spain', address='Beach Road 9', stars=5, latitude=41.97, longitude=2.82, description='Курортний готель біля моря.')
    hotel3 = Hotel(chain_id=chain2.id, name='Nordic Escape Oslo Hub', city='Oslo', country='Norway', address='Fjord Gate 21', stars=4, latitude=59.91, longitude=10.75, description='Комфортний готель для міських подорожей.')
    db.session.add_all([hotel1, hotel2, hotel3])
    db.session.flush()

    rooms = [
        Room(hotel_id=hotel1.id, room_number='101', room_type='Standard', capacity=2, price_per_night=90, is_available=True, has_breakfast=False),
        Room(hotel_id=hotel1.id, room_number='102', room_type='Deluxe', capacity=3, price_per_night=140, is_available=True, has_breakfast=True),
        Room(hotel_id=hotel2.id, room_number='201', room_type='Suite', capacity=4, price_per_night=220, is_available=True, has_breakfast=True),
        Room(hotel_id=hotel3.id, room_number='301', room_type='Business', capacity=2, price_per_night=160, is_available=True, has_breakfast=True),
    ]
    db.session.add_all(rooms)

    customer1 = Customer(full_name='Anna Melnyk', email='anna@example.com', phone='+380971112233', loyalty_level='Gold')
    customer2 = Customer(full_name='Taras Kovalenko', email='taras@example.com', phone='+380631234567', loyalty_level='Standard')
    db.session.add_all([customer1, customer2])
    db.session.flush()

    reviews = [
        Review(hotel_id=hotel1.id, customer_id=customer1.id, rating=9, comment='Чисті кімнати та зручна локація.'),
        Review(hotel_id=hotel1.id, customer_id=customer2.id, rating=8, comment='Добрий сервіс, але мало паркомісць.'),
        Review(hotel_id=hotel3.id, customer_id=customer1.id, rating=10, comment='Дуже сподобався сніданок і персонал.'),
    ]
    db.session.add_all(reviews)

    db.session.commit()
