FROM nginxinc/nginx-unprivileged:1-alpine
Label maintainer="krasenhristov"

# storing default.conf.tpl, uwsgi_params and our run script in the image
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static && \

    # give nginx user access to the static folder
    chmod 755 /vol/static && \

    # create an empty file and give nginx user access to it
    touch /etc/nginx/conf.d/default.conf && \

    # give nginx user access to the file just created
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \

    # make the run script executable
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]
