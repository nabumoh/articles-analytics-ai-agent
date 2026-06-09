-- Run these commands in MindsDB SQL Editor (http://localhost:47334)

CREATE DATABASE articles_pg
WITH ENGINE = 'postgres',
PARAMETERS = {
  "host": "db",
  "port": 5432,
  "database": "articles_db",
  "user": "postgres",
  "password": "postgres"
};

-- For free local setup, run Ollama on your machine and use provider 'ollama'.
CREATE AGENT articles_qa_agent
USING model = {
  'provider': 'ollama',
  'model_name': 'llama3.1',
  'base_url': 'http://host.docker.internal:11434/v1'
};

-- Example ask:
-- SELECT answer FROM mindsdb.articles_qa_agent WHERE question = 'How many articles are from TechDaily?';
