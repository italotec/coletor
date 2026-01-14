import os
from flask import Blueprint, render_template, current_app, request
from flask_login import login_required, current_user
from .services import read_accounts

accounts_bp = Blueprint("accounts", __name__)

def _root_domain_from_host(host: str) -> str:
    """
    Extracts root domain from a hostname.
    Example:
      sistema.scopebrazil.com -> scopebrazil.com
    """
    host = (host or "").split(":")[0].strip().lower()
    if not host:
        return host

    if host in ("localhost", "127.0.0.1"):
        return host

    parts = host.split(".")
    if len(parts) < 2:
        return host

    return parts[-2] + "." + parts[-1]


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


@accounts_bp.get("/links")
@login_required
def links_page():
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.host or ""
    host_no_port = host.split(":")[0]

    root_domain = _root_domain_from_host(host_no_port)

    # ONLY root domain link
    root_link = f"{proto}://{root_domain}/?ref={current_user.id}"

    return render_template(
        "links.html",
        title="Links",
        link=root_link,
        root_domain=root_domain
    )
