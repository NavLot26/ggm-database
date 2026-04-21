from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")

