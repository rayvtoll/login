FROM python:3.7-alpine
RUN apk add -U curl iputils
RUN pip3 install --upgrade pip && pip3 install flask requests
WORKDIR /app
COPY . /app
EXPOSE 5001
ENTRYPOINT ["python3"]
CMD ["app.py"]
