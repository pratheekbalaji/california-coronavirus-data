FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD resulting.py /app
ADD latimes-state-totals.csv /app
ADD cdph-race-ethnicity.csv /app
CMD ["bokeh","serve","--show", "/app/resulting.py"]
