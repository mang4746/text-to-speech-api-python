#
FROM python:3.12.1

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt
COPY ./banner.txt /code/banner.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./VERSION /code/VERSION
COPY ./run.py /code/
COPY ./app /code/app

#
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
CMD ["python", "run.py"]
