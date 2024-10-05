FROM mongo:4

WORKDIR /config
COPY wait-for-it.sh mongo-setup.js mongo-setup.sh /config/
CMD [ "bash", "-c", "/config/wait-for-it.sh mongodb1:27017 -- /config/mongo-setup.sh"]
