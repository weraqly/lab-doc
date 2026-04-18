from flask import Blueprint, render_template, request, redirect, url_for
from ..models import db
from ..models.entities import Review, Hotel, Customer

review_bp = Blueprint('reviews', __name__)


@review_bp.route('/')
def list_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('reviews/list.html', reviews=reviews)


@review_bp.route('/create', methods=['GET', 'POST'])
def create_review():
    hotels = Hotel.query.order_by(Hotel.name).all()
    customers = Customer.query.order_by(Customer.full_name).all()
    if request.method == 'POST':
        review = Review(
            hotel_id=int(request.form['hotel_id']),
            customer_id=int(request.form['customer_id']),
            rating=int(request.form['rating']),
            comment=request.form['comment']
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('reviews.list_reviews'))
    return render_template('reviews/form.html', review=None, hotels=hotels, customers=customers)


@review_bp.route('/<int:review_id>/edit', methods=['GET', 'POST'])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    hotels = Hotel.query.order_by(Hotel.name).all()
    customers = Customer.query.order_by(Customer.full_name).all()
    if request.method == 'POST':
        review.hotel_id = int(request.form['hotel_id'])
        review.customer_id = int(request.form['customer_id'])
        review.rating = int(request.form['rating'])
        review.comment = request.form['comment']
        db.session.commit()
        return redirect(url_for('reviews.list_reviews'))
    return render_template('reviews/form.html', review=review, hotels=hotels, customers=customers)


@review_bp.route('/<int:review_id>/delete', methods=['POST'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('reviews.list_reviews'))
