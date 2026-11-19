FROM python:3.12-bookworm

ARG ODOO_REVISION=3911d7a43947d7da043897c4e403f3720543dc6c

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        git libldap2-dev libpq-dev libsasl2-dev \
    && rm -rf /var/lib/apt/lists/* \
    && git init /opt/odoo \
    && git -C /opt/odoo fetch --depth 1 https://github.com/odoo/odoo.git "$ODOO_REVISION" \
    && git -C /opt/odoo checkout --detach FETCH_HEAD \
    && rm -rf /opt/odoo/.git \
    && pip install --no-cache-dir -r /opt/odoo/requirements.txt \
    && pip install --no-cache-dir watchdog==6.0.0 \
    && useradd --create-home odoo \
    && mkdir -p /var/lib/odoo \
    && chown odoo:odoo /var/lib/odoo

COPY odoo.conf /etc/odoo.conf
USER odoo
WORKDIR /opt/odoo
ENV ODOO_RC=/etc/odoo.conf PYTHONIOENCODING=UTF-8
ENTRYPOINT ["python3", "/opt/odoo/odoo-bin"]
