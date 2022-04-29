From ubuntu:latest
ADD . /



RUN apt-get update && \
    apt-get -y install cron
RUN apt-get -y install python3-pip
RUN pip3 install requests && \
    pip3 install PyYAML

RUN apt-get update  && \
    apt-get install nano
RUN chmod 0777 /data.py

RUN chmod 0777 /project_env.sh


RUN touch /var/log/cron.log
RUN crontab crontab

CMD bash /project_env.sh && /etc/init.d/cron start && tail -f /var/log/cron.log
# Add the cron job
#RUN crontab -l | { cat; echo "*/2 * * * * /usr/local/bin/python3 /data.py > /output.txt"; } | crontab -

# Run the command on container startup
#CMD ["cron", "-f"]
