from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.dashboard"))
    return render_template("login.html", title="Login")

@auth_bp.post("/login")
def login_post():
    username = (request.form.get("username") or "").strip()
    password = (request.form.get("password") or "").strip()

    u = User.query.filter_by(username=username).first()
    if not u or not u.check_password(password):
        flash("Usuário ou senha inválidos.", "error")
        return redirect(url_for("auth.login"))

    if u.is_banned:
        flash("Este usuário está banido.", "error")
        return redirect(url_for("auth.login"))

    login_user(u)
    return redirect(url_for("accounts.dashboard"))

@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
