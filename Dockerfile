FROM python:3.9-buster
ENV APP_DIR=/app
WORKDIR $APP_DIR
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs && apt-get clean

COPY app/package.json app/package-lock.json $APP_DIR/
RUN npm install

COPY app/requirements.txt $APP_DIR/
RUN pip install -r requirements.txt --use-deprecated=legacy-resolver

COPY scripts/docker_build_step2.sh /root/
COPY app/ $APP_DIR/
RUN bash /root/docker_build_step2.sh

ARG TAG_ARG
ARG BUILD_ARG
ENV TAG=$TAG_ARG
ENV BUILD=$BUILD_ARG

EXPOSE 8000
CMD ["/app/ops/web_launch.sh"]
