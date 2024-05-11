from flask import Blueprint, render_template

from . import service

index = Blueprint("index", __name__)


@index.route("/")
def get_all():
    return render_template("index.html")


@index.route("/poll")
@index.route("/search")
def get_poll():
    return render_template("react.html")