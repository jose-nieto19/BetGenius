FROM python:3.7

RUN mkdir /Bot_BetGenius_Estandar
WORKDIR /Bot_BetGenius_Estandar
ADD . /Bot_BetGenius_Estandar/
RUN pip install -r requeriments.txt

EXPOSE 5000 
CMD ["python","/Bot_BetGenius_Estandar/Bot_BetGenius_Estandar.py"]