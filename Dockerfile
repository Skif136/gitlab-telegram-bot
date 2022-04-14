FROM python:3.9.12

COPY ./* /work/
WORKDIR /work

RUN pip install --upgrade pip && \
    pip install flask && \
    pip install requests &&\
    pip install ipdb

EXPOSE 10111
CMD python app.py