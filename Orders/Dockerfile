#Usa uma linguagem base do python
FROM python:3.9-slim

#Define o diretorio de trabalho dentro do container
WORKDIR /app

#Copia os ficheiros necessários para o container
COPY . /app

#Instala as dependencias
RUN pip install -r requirements.txt

#Expoe a porta que o microserviço utiliza
EXPOSE 5004

#Comando para iniciar o serviço.
CMD ["python","app.py"]