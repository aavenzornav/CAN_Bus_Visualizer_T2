from flask import Flask, render_template, request, flash
from web import app, db
from .forms import create_project_form
from datetime import datetime
from werkzeug.utils import redirect


@app.route('/')
def homepage():
    return render_template('base.html', title='Home')

#create project will be stored in mongo db
@app.route('/manage-project', methods = ["POST", "GET"])
def create_project():
    if request.method == "POST":
        form = create_project_form(request.form)
        todo_user_initials = form.user_initials.data
        todo_event_name = form.event_name.data
        todo_can_connector_id = form.can_connector_id.data
        todo_vehicle_id = form.vehicle_id.data
        todo_baud_rate = form.baud_rate.data
        todo_can_dbc = form.can_dbc.data

        db.project.insert_one({
            "user_initials": todo_user_initials,
            "event_name": todo_event_name,
            "can_connector_id": todo_can_connector_id,
            "vehicle id": todo_vehicle_id,
            "baud_rate": todo_baud_rate,
            "can_dbc": todo_can_dbc
        })
        flash("added", "success")
        return redirect("/")
    else:
        form = create_project_form()
    return render_template('manage-project.html', title='Create Project', form=form)

@app.route('/open-project')

def open_project():
    return render_template('open-project.html', title='Open Existing Project')

@app.route('/sync-project')

def sync_project():
    return render_template('sync-project.html', title='Sync Project')

@app.route('/archive-project')

def archive_project():
    return render_template('archive-project.html', title='Archive Project')

@app.route('/can-bus-manager')

def can_bus_manager():
    return render_template('can-bus-manager.html', title='CAN Bus Manager')


