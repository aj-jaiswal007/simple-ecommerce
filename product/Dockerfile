# Using python  3.9 Image
FROM python:3.9

# This is our working directory
WORKDIR /code

# requirements.txt are in our working directly
COPY ./requirements.txt /code/requirements.txt

# installing requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copiyfing our code
COPY ./product /code/product
COPY ./common /code/common



# running server
CMD ["uvicorn", "product.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8081"]
