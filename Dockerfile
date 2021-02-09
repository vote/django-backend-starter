FROM python:3.9-buster

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    pip install pipenv==2020.11.15 && \
    apt-get clean

ENV APP_DIR=/app
WORKDIR $APP_DIR

COPY app/package.json app/package-lock.json $APP_DIR/
RUN npm install

COPY app/Pipfile app/Pipfile.lock $APP_DIR/
RUN pipenv install

COPY scripts/docker_build_step2.sh /root/
COPY app/ $APP_DIR/
RUN bash /root/docker_build_step2.sh && rm /root/docker_build_step2.sh

ARG TAG_ARG
ARG BUILD_ARG
ENV TAG=$TAG_ARG
ENV BUILD=$BUILD_ARG

EXPOSE 8000
CMD ["/app/ops/web_launch.sh"]
