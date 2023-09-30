#!/usr/bin/python3
"""A new view for Place objects that handlees all default
RESTFUL API actions"""
from flask import Flask, jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_city_id(city_id):
    """Returns place or places given it's/their
    City id if found else return 404"""
    city = storage.get(City, city_id)
    if city:
        places = [p.to_dict() for p in city.places]
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_place_id(place_id):
    """Return a place given it's place id else 404"""
    place = storage.get(Place, place_id)
    return jsonify(place.to_dict()) if place else abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_object(place_id):
    """Deletes a Place object if found otherwise return 404"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_obj_by_city_id(city_id):
    """Creates a place object given a city id if city id is not
    linked to a city object return 404"""
    if not storage.get(City, city_id):
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if ("user_id" in data and not storage.get(User, data.get("user_id"))):
        abort(404)

    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    place = Place(**data, city_id=city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object based on the place id"""
    fetch_place = storage.get(Place, place_id)
    if fetch_place:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        keep = ["id", "created_at", "updated_at", "user_id", "city_id"]
        for key, values in data.items():
            if key not in keep:
                setattr(fetch_place, key, values)
        fetch_place.save()
        return jsonify(fetch_place.to_dict()), 200
    else:
        abort(404)