FROM python:latest
RUN python -m pip install --upgrade pip
RUN python --version && pip --version

ENV PYTHONUNBUFFERED 1

RUN mkdir fightfinder-backend
WORKDIR fightfinder-backend

ADD . /fightfinder-backend
#RUN addgroup -S adifect-app && adduser -S adifect-app -G adifect-app
RUN pip install --no-cache-dir -r requirements.txt && \
        pip install gunicorn
        

RUN python manage.py collectstatic

RUN chmod +x gunicorn.sh
EXPOSE 8000
ENTRYPOINT ["./gunicorn.sh"]
