FROM python:3.11
RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
WORKDIR /app
COPY . .
RUN /root/.local/bin/pdm install
EXPOSE 8501
CMD /root/.local/bin/pdm run streamlit run main.py
