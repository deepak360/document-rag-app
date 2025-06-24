FROM ollama/ollama

RUN ollama pull mistral

CMD ["ollama", "serve"]
