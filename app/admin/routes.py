from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from datetime import datetime
from ..extensions import db
from ..models import User
from ..accounts.services import stats_for_ref, read_accounts

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def _admin_only():
    if not current_user.is_authenticated:
        abort(403)
    if not current_user.is_admin:
        abort(403)

@admin_bp.get("/users")
@login_required
def admin_users():
    _admin_only()
    users = User.query.order_by(User.id.asc()).all()

    dat_path = current_app.config["USERNAMES_DAT"]
    stats = {}
    now = datetime.now()
    for u in users:
        stats[u.id] = stats_for_ref(dat_path, u.id, now=now)

    return render_template("admin_users.html", title="Admin • Usuários", users=users, stats=stats)

@admin_bp.post("/users/create")
@login_required
def admin_create_user():
    _admin_only()
    username = (request.form.get("username") or "").strip()
    password = (request.form.get("password") or "").strip()

    if not username or not password:
        flash("Informe username e password.", "error")
        return redirect(url_for("admin.admin_users"))

    if User.query.filter_by(username=username).first():
        flash("Esse username já existe.", "error")
        return redirect(url_for("admin.admin_users"))

    u = User(username=username, is_admin=False, is_banned=False)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()

    flash("Usuário criado com sucesso.", "ok")
    return redirect(url_for("admin.admin_users"))

@admin_bp.post("/users/<int:user_id>/toggle-ban")
@login_required
def admin_toggle_ban(user_id):
    _admin_only()
    u = User.query.get_or_404(user_id)

    if u.is_admin:
        flash("Não é possível banir um admin.", "error")
        return redirect(url_for("admin.admin_users"))

    u.is_banned = not u.is_banned
    db.session.commit()

    flash("Status atualizado.", "ok")
    return redirect(url_for("admin.admin_users"))

@admin_bp.get("/users/<int:user_id>")
@login_required
def admin_user_detail(user_id):
    _admin_only()
    u = User.query.get_or_404(user_id)

    dat_path = current_app.config["USERNAMES_DAT"]
    rows = read_accounts(dat_path, ref_id=u.id)

    return render_template("admin_user_detail.html", title=f"Admin • {u.username}", u=u, rows=rows)
