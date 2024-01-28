from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from elearning .auth import login_required
from elearning .db import get_db

bp = Blueprint('report', __name__)
