# Usar uma imagem oficial do Python
FROM python:3.11-slim

# Setar o diretório de trabalho
WORKDIR /chat

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta 8501 para o Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
