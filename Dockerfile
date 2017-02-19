FROM python:3.4

RUN pip install scikit-learn numpy scipy pandas --upgrade

WORKDIR /src
