FROM python:3.12-bookworm

ARG ODOO_REVISION=3911d7a43947d7da043897c4e403f3720543dc6c

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl libldap2-dev libpq-dev libsasl2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fL --retry 1 --retry-all-errors --connect-timeout 30 \
        "https://codeload.github.com/odoo/odoo/tar.gz/$ODOO_REVISION" \
        -o /tmp/odoo.tar.gz \
    && mkdir -p /opt/odoo \
    && tar -xzf /tmp/odoo.tar.gz -C /opt/odoo --strip-components=1 \
    && rm /tmp/odoo.tar.gz

RUN pip install --no-cache-dir -r /opt/odoo/requirements.txt \
    && pip install --no-cache-dir watchdog==6.0.0 \
    && useradd --create-home odoo \
    && mkdir -p /var/lib/odoo \
    && chown odoo:odoo /var/lib/odoo

COPY odoo.conf /etc/odoo.conf
USER odoo
WORKDIR /opt/odoo
ENV ODOO_RC=/etc/odoo.conf PYTHONIOENCODING=UTF-8
ENTRYPOINT ["python3", "/opt/odoo/odoo-bin"]
