FROM python:3.9.5-slim-buster

ENV APP_USER=technest
ENV APP_SRC=/opt/technest
ENV PATH="/home/${APP_USER}/.local/bin:${PATH}"
ARG APP_REQUIREMENTS=requirements.txt
ENV APP_CSV_PATH="${APP_SRC}/data/NBA2021.csv"
ENV PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=2 PYTHONUTF8=1

RUN groupadd -r ${APP_USER} && \
    useradd --no-log-init --create-home -r -g ${APP_USER} ${APP_USER}
USER ${APP_USER}
WORKDIR ${APP_SRC}

COPY --chown=${APP_USER}:${APP_USER} ./requirements.txt ./${APP_REQUIREMENTS} ./
COPY --chown=${APP_USER}:${APP_USER} ./data/NBA2021.csv ${APP_CSV_PATH}

RUN python -m pip install --no-cache --upgrade pip && \
    python -m pip install --no-cache -r "${APP_REQUIREMENTS}"

COPY --chown=${APP_USER}:${APP_USER} ./app ./app
COPY --chown=${APP_USER}:${APP_USER} ./templates ./templates
COPY --chown=${APP_USER}:${APP_USER} ./static ./static
COPY --chown=${APP_USER}:${APP_USER} production/* ./

CMD ["./start.sh"]
