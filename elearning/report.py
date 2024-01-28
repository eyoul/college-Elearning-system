from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from elearning .auth import login_required
from elearning .db import get_db

bp = Blueprint('report', __name__)

"""
Student Must registr for major 
    the student will nee only his/her grade 
Lecturer rigistrer the student 
    input grade 
    view all student 
    update all student grade 
    crud posts on dashboard 
    
"""
