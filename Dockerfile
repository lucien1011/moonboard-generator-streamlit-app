# app/Dockerfile

FROM python:3.9-slim

WORKDIR app/

COPY ./app .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN ls ./

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
