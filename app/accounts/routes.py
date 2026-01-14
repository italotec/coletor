import os
from flask import Blueprint, render_template, current_app, request
from flask_login import login_required, current_user
from .services import read_accounts

accounts_bp = Blueprint("accounts", __name__)

def _root_domain_from_host(host: str) -> str:
    """
    Extracts root domain from a hostname.
    Example:
      sistema.verificacaopro.com -> verificacaopro.com

    Notes:
    - This uses the "last 2 labels" approach.
    - Good for verificacaopro.com style domains.
    - If host is localhost/127.0.0.1 or has no dots, returns host itself.
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
    # Determine scheme properly behind nginx (X-Forwarded-Proto)
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)

    host = request.host or ""
    host_no_port = host.split(":")[0]
    root_domain = _root_domain_from_host(host_no_port)

    # Root domain link + ref
    root_link = f"{proto}://{root_domain}/?ref={current_user.id}"

    # Also provide current host link (subdomain) + ref (optional but useful)
    current_link = f"{proto}://{host_no_port}/?ref={current_user.id}"

    links = [
        {"label": "Link principal (root domain)", "url": root_link},
        {"label": "Link do subdomínio atual", "url": current_link},
    ]

    return render_template(
        "links.html",
        title="Links",
        links=links,
        root_domain=root_domain,
        host=host_no_port,
        proto=proto
    )
