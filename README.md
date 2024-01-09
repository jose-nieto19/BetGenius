# isi-BetGenius

Landing Page de nuestro proyecto: https://betgenius.jimdosite.com/

Para ejecutar el Bot Estandar:

$ docker build -f dockerfile -t estandar:latest .
$ docker run -p 2001:5000 -i estandar

Para ejecutar el Bot Premium:

$ docker build -f dockerfile2 -t premium:latest .
$ docker run -p 2000:5001 -i premium

Es necesario ejecutar cada uno en una terminal diferente.
