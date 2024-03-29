FROM alpine:3.18.0
ENV DESTDIR /usr/local/bin/
RUN apk add --no-cache curl openssh-client python3
RUN mkdir /root/.ssh && chmod 700 /root/.ssh
COPY main.py ${DESTDIR}
WORKDIR ${DESTDIR}
CMD ["/usr/bin/python3", "-u", "mainpy.my"]
