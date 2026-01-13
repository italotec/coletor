from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from .services import read_accounts

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.get("/")
@login_required
def dashboard():
    dat_path = current_app.config["USERNAMES_DAT"]
    rows = read_accounts(dat_path, ref_id=current_user.id)

    return render_template(
        "dashboard.html",
        title="Dashboard",
        rows=rows
    )
