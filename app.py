from flask import Flask, request, jsonify
from datetime import datetime, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, RequestLog, Base
import os
import json

app = Flask(__name__)

# Read the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for Flask application")

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Sample data
if session.query(Restaurant).count() == 0:
    sample_data = [
        Restaurant(name="Veggie Delight", address="1", style="Italian", vegetarian=True, opening_hour=time(9, 0), closing_hour=time(21, 0), deliveries=True),
        Restaurant(name="French Gourmet", address="2", style="French", vegetarian=False, opening_hour=time(11, 0), closing_hour=time(23, 0), deliveries=False),
    ]
    session.add_all(sample_data)
    session.commit()

@app.route('/recommend', methods=['GET'])
def recommend_restaurant():
    style = request.args.get('style')
    vegetarian = request.args.get('vegetarian')
    deliveries = request.args.get('deliveries')
    current_time = datetime.now().time()
    
    query = session.query(Restaurant)
    
    if style:
        query = query.filter(Restaurant.style.ilike(f"%{style}%"))
    if vegetarian:
        query = query.filter(Restaurant.vegetarian == (vegetarian.lower() == 'yes'))
    if deliveries:
        query = query.filter(Restaurant.deliveries == (deliveries.lower() == 'yes'))
    
    query = query.filter(Restaurant.opening_hour <= current_time, Restaurant.closing_hour >= current_time)
    
    restaurant = query.first()
    
    if restaurant:
        response = {
            'name': restaurant.name,
            'address': restaurant.address,
            'style': restaurant.style,
            'vegetarian': restaurant.vegetarian,
            'opening_hour': restaurant.opening_hour.strftime("%H:%M"),
            'closing_hour': restaurant.closing_hour.strftime("%H:%M"),
            'deliveries': restaurant.deliveries
        }
    else:
        response = {'message': 'No restaurant found matching the criteria'}
    
    log_request_and_response(request.args, response)
    return jsonify(response)

@app.route('/restaurants', methods=['GET'])
def list_restaurants():
    restaurants = session.query(Restaurant).all()
    response = [{
        'name': r.name,
        'address': r.address,
        'style': r.style,
        'vegetarian': r.vegetarian,
        'opening_hour': r.opening_hour.strftime("%H:%M"),
        'closing_hour': r.closing_hour.strftime("%H:%M"),
        'deliveries': r.deliveries
    } for r in restaurants]
    log_request_and_response(request.args, response)
    return jsonify(response)

def log_request_and_response(request_data, response_data):
    log_entry = RequestLog(
        request_data=json.dumps(request_data),
        response_data=json.dumps(response_data)
    )
    session.add(log_entry)
    session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
