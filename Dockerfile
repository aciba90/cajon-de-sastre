FROM python:3.9.5-slim-buster

ENV APP_USER=technest
ENV PATH="/home/${APP_USER}/.local/bin:${PATH}"

RUN groupadd -r ${APP_USER} && \
    useradd --no-log-init --create-home -r -g ${APP_USER} ${APP_USER}
USER ${APP_USER}

COPY --chown=${APP_USER}:${APP_USER} ./requirements.txt /requirements.txt
RUN python -m pip install --no-cache --upgrade pip && \
    python -m pip install --no-cache -r /requirements.txt

EXPOSE 5000
COPY --chown=${APP_USER}:${APP_USER} ./app /app
COPY --chown=${APP_USER}:${APP_USER} ./templates /templates

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
