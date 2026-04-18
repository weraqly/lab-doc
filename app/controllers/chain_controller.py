from flask import Blueprint, render_template, request, redirect, url_for
from ..models import db
from ..models.entities import HotelChain
from ..services.hotel_service import HotelService

chain_bp = Blueprint('chains', __name__)


@chain_bp.route('/')
def list_chains():
    chains = HotelChain.query.order_by(HotelChain.name).all()
    return render_template('chains/list.html', chains=chains)


@chain_bp.route('/create', methods=['GET', 'POST'])
def create_chain():
    if request.method == 'POST':
        HotelService.create_chain({
            'name': request.form['name'],
            'api_provider': request.form['api_provider'],
            'integration_status': request.form['integration_status'],
            'country': request.form['country'],
        })
        return redirect(url_for('chains.list_chains'))
    return render_template('chains/form.html', chain=None)


@chain_bp.route('/<int:chain_id>/edit', methods=['GET', 'POST'])
def edit_chain(chain_id):
    chain = HotelChain.query.get_or_404(chain_id)
    if request.method == 'POST':
        chain.name = request.form['name']
        chain.api_provider = request.form['api_provider']
        chain.integration_status = request.form['integration_status']
        chain.country = request.form['country']
        db.session.commit()
        return redirect(url_for('chains.list_chains'))
    return render_template('chains/form.html', chain=chain)


@chain_bp.route('/<int:chain_id>/delete', methods=['POST'])
def delete_chain(chain_id):
    chain = HotelChain.query.get_or_404(chain_id)
    db.session.delete(chain)
    db.session.commit()
    return redirect(url_for('chains.list_chains'))
