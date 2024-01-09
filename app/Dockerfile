FROM python:3.10
ENV STATIC_URL /static
ENV STATIC_PATH /static
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=views.py
CMD ["flask", "run", "--host", "0.0.0.0"]