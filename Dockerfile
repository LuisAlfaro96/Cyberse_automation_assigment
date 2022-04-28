From python:3
ADD . /

RUN chmod 0644 /data.py

RUN apt-get update && \
    apt-get -y install cron

RUN pip3 install requests && \
    pip3 install PyYAML

RUN apt-get update  && \
    apt-get install nano

# Add the cron job
RUN crontab -l | { cat; echo "*/2 * * * * /usr/local/bin/python3 /data.py"; } | crontab -

# Run the command on container startup
CMD ["cron", "-f"]
