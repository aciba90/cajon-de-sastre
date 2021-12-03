FROM mongo:4

WORKDIR /config

COPY wait-for-it.sh mongo-setup.js mongo-setup.sh /config/
# RUN chmod +x /config/wait-for-it.sh
# RUN chmod +x /config/mongo-setup.sh
CMD [ "bash", "-c", "/config/wait-for-it.sh mongodb1:27017 -- /config/mongo-setup.sh"]
