FROM python:2.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /
WORKDIR /
EXPOSE 5000
CMD ["python", "RohBot/bot.py"]