FROM alpine
RUN apk add --update py-pip python build-base openldap-dev python2-dev && pip install requests django-auth-ldap
RUN pip install --upgrade django
WORKDIR /app
COPY . /app
EXPOSE 5001
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:5001"]
