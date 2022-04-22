import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app, jsonify
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename, redirect

from flaskApp.db import db
from flaskApp.db.models import Location
from flaskApp.songs.forms import csv_upload
from flask_login import current_user, login_required

map = Blueprint('map', __name__, template_folder='templates')
@map.route('/locations', methods=['GET'], defaults={"page": 1})
@map.route('/locations/<int:page>', methods=['GET'])
def browse_locations(page):
    page = page
    per_page = 10
    pagination = Location.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_locations.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@map.route('/locations_datatables/', methods=['GET'])
def browse_locations_datatables():

    data = Location.query.all()

    try:
        return render_template('browse_locations_datatables.html',data=data)
    except TemplateNotFound:
        abort(404)

@map.route('/api/locations/', methods=['GET'])
def api_locations():
    data = current_user.locations
    try:
        return jsonify(data=[location.serialize() for location in data])
    except TemplateNotFound:
        abort(404)

@map.route('/locations/map', methods=['GET'])
def map_locations():
    google_api_key = current_app.config.get('GOOGLE_API_KEY')
    log = logging.getLogger("myApp")
    log.info(google_api_key)
    try:
        return render_template('map_locations.html',google_api_key=google_api_key)
    except TemplateNotFound:
        abort(404)



@map.route('/locations/upload', methods=['POST', 'GET'])
@login_required
def location_upload():
    form = csv_upload()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        list_of_locations = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_locations.append(Location(row['location'],row['longitude'],row['latitude'],row['population']))
        current_user.locations = list_of_locations
        db.session.commit()
        return redirect(url_for('map.browse_locations'))

    def edit_location(id):
        location = Location.query.get(id)
        form = user_edit_form(obj=location)
        if form.validate_on_submit():
            location.title = form.title.data
            location.longitude = form.longitude.data
            location.latitude = form.latitude.data
            location.population = int(form.population.data)
            db.session.add(location)
            db.session.commit()
            flash("Location Info Edited Successfully",'Success!')
            return redirect(url_for('browse_locations'))
        return render_template('edit_location.html', form=form)

    @map.route('/locations/delete', methods=['POST'])
    @login_required
    def delete_location(user_id):
        location = Location.query.get(user_id)
        if user.id == current_user.id:
            flash("You can't delete yourself!")
            return redirect(url_for('browse_locations'), 302)
        db.session.delete(location)
        db.session.commit()
        flash("Location Deleted", 'Success!')
        return redirect(url_for('auth.browse_users'), 302)