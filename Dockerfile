FROM fedora:38
EXPOSE 5000

ENV PATH="/root/.local/bin:$PATH"
RUN set -x \
    && dnf -y update \
    && dnf -y install python3-pip \
    && dnf clean all \
    && rm -rf /var/cache/yum

COPY . /app
WORKDIR /app
RUN ln -s /usr/bin/python3 /usr/bin/python \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version \
    && python3 -m pip install pip --upgrade \
    && poetry config cache-dir /app \
    && poetry config virtualenvs.in-project true \
    && poetry config installer.max-workers 10 \
    && poetry config --list \
    && poetry install

ENTRYPOINT ["poetry", "run", "python3", "app/app.py"]
