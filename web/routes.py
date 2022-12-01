from flask import Flask, render_template, request, flash
from web import app
import os
import subprocess
from . import db
from .forms import create_project_form, create_node, sync_form
from datetime import datetime
from werkzeug.utils import redirect
from web import Network


node_list = []
@app.route('/')
def homepage():
    return render_template('base.html', title='Home')

@app.route('/open-project')
def open_project():
    #same as node-map1 method;
    #this will make it possible to retrieve ALL the collections in the project db
    todos = []
    for todo in db.project.find().sort("user_initials", -1):
        todo["_id"] = str(todo["_id"])
        todos.append(todo)
    #info = db.project.find()
    return render_template('open-project.html', title='Open Existing Project', todos = todos)
@app.route('/node-map1')
def node_map1():
    todos = []
    todo = db.project.find_one({"event_name":  "Proj1"})
    # info = db.project.find()
    todos.append(todo)
    return render_template('node-map1.html', title='Open Existing Project', todos=todos)

#create project will be stored in mongo db
@app.route('/manage-project', methods = ("POST", "GET"))
def manage_project():
   
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
        flash("user initials", "event name")
        return redirect('/')
    else:
        form = create_project_form(request.form)
    #print(db.project.find_one())
    return render_template('manage-project.html', title='Create Project', form=form)


@app.route('/sync-project', methods = ("POST", "GET"))
def sync_project():


    if request.method == "GET":
        print("hello")
        form = sync_form(request.form)
        argstwo = ["rsync" , 'web/src/j1939_1.dbc' , 'web/dest/hello.dbc']
        subprocess.call(argstwo);
        return render_template('sync-project.html', title='Sync Project', srcPath='/web/lib/projects', form=form)

    else:
        form = sync_form(request.form)
        return render_template('sync-project.html', title='Sync Project', srcPath='/web/lib/projects', form=form)

@app.route("/node_map", methods = ("POST", "GET"))
def node_map():
    print("enter")
    #print(node_list)
    #mapper(node_list)
    return render_template('Network.py', title='CAN Bus Map')
@app.route('/can-bus-manager', methods = ("POST", "GET"))
def can_bus_manager():
    if request.method == "POST":
        form = create_node(request.form)
        todo_node_name = form.node_name.data
        node_list.append(todo_node_name)
        #print("befor ret")
        Network.mapper(node_list)
        return redirect('/')
    else:
        form = create_node(request.form)
    return render_template('can-bus-manager.html', title='CAN Bus Manager',form = form)

@app.route('/view-traffic')

def view_traffic():
    return render_template('view-traffic.html', title='View Traffic')

@app.route('/tags')

def tag_nodes():
    return render_template('tag_nodes.html', title='Sync Project', nID='0x7E5', blStatus = 'False')




