#!/usr/bin/env python3

import os
import json
import requests
import redis
from datetime import datetime, date
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Read API key from env file
def load_api_key():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    try:
        with open(env_path, 'r') as f:
            content = f.read()
            for line in content.strip().split('\n'):
                if line.startswith('FIXER_API_KEY='):
                    return line.split('=', 1)[1]
    except FileNotFoundError:
        logger.error(f"Environment file not found: {env_path}")
    return None

FIXER_API_KEY = load_api_key()
if not FIXER_API_KEY:
    logger.error("FIXER_API_KEY not found in env file")
    exit(1)

# Redis setup
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    logger.info("Connected to Redis")
except redis.ConnectionError:
    logger.error("Could not connect to Redis. Make sure Redis is running.")
    exit(1)

# Cache configuration
CACHE_KEY_PREFIX = "exchange_rates"
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds

def get_today_cache_key():
    """Generate cache key for today's exchange rates"""
    today = date.today().isoformat()
    return f"{CACHE_KEY_PREFIX}_{today}"

def calculate_rates_with_base(eur_rates, new_base):
    """
    Calculate exchange rates with a different base currency
    
    Args:
        eur_rates (dict): Exchange rates with EUR as base
        new_base (str): New base currency code
    
    Returns:
        dict: Exchange rates with new base currency
    """
    if new_base not in eur_rates['rates']:
        raise ValueError(f"Currency {new_base} not found in rates")
    
    base_rate = eur_rates['rates'][new_base]
    new_rates = {}
    
    for currency, rate in eur_rates['rates'].items():
        new_rates[currency] = rate / base_rate
    
    return {
        'success': True,
        'timestamp': eur_rates['timestamp'],  # Preserve original timestamp
        'base': new_base,
        'date': eur_rates['date'],  # Preserve original date
        'rates': new_rates
    }

def fetch_from_fixer_api():
    """Fetch exchange rates from Fixer API"""
    url = "https://data.fixer.io/api/latest"
    params = {
        'access_key': FIXER_API_KEY,
        'symbols': 'USD,EUR,PLN,GTQ'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('success'):
            raise Exception(f"Fixer API error: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching from Fixer API: {e}")
        raise

@app.route('/api/rates', methods=['GET'])
def get_exchange_rates():
    """Get exchange rates with optional base currency conversion"""
    try:
        base_currency = request.args.get('base', 'PLN').upper()
        today_key = get_today_cache_key()
        
        # Check cache first
        cached_data = redis_client.get(today_key)
        
        if cached_data:
            logger.info("Using cached exchange rates")
            eur_based_rates = json.loads(cached_data)
        else:
            logger.info("Fetching fresh exchange rates from Fixer API")
            eur_based_rates = fetch_from_fixer_api()
            
            # Cache the EUR-based rates
            redis_client.setex(
                today_key, 
                CACHE_DURATION, 
                json.dumps(eur_based_rates)
            )
            logger.info("Cached exchange rates for today")
        
        # If base currency is EUR, return as-is
        if base_currency == 'EUR':
            return jsonify(eur_based_rates)
        
        # Calculate rates with requested base currency
        converted_rates = calculate_rates_with_base(eur_based_rates, base_currency)
        return jsonify(converted_rates)
        
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return jsonify({
            'success': False,
            'error': 'Invalid currency',
            'message': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f"Error getting exchange rates: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch exchange rates',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        redis_client.ping()
        redis_status = 'connected'
    except Exception:
        redis_status = 'disconnected'
    
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'redis': redis_status
    })

@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear today's cache (for testing purposes)"""
    try:
        today_key = get_today_cache_key()
        deleted = redis_client.delete(today_key)
        return jsonify({
            'success': True,
            'message': f"Cache cleared. Deleted {deleted} keys."
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting exchange rate proxy server...")
    logger.info(f"Fixer API Key: {'*' * (len(FIXER_API_KEY) - 4)}{FIXER_API_KEY[-4:]}")
    app.run(host='0.0.0.0', port=8001, debug=False)