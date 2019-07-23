FROM alpine
RUN apk add --update py-pip python && pip install requests  
RUN pip install --upgrade django
WORKDIR /app
COPY . /app
EXPOSE 5001
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:5001"]
