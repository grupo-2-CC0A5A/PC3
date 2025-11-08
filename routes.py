from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from datetime import datetime
from decimal import Decimal
from models import GestorAlquileres

rental_bp = Blueprint('rentals', __name__)
gestor = GestorAlquileres()

@rental_bp.route('/')
def index():
    return {
        'message': 'ok'
    }
