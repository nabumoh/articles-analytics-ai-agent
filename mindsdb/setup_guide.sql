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

-- This agent structure may vary by MindsDB version.
-- If CREATE AGENT syntax differs, use MindsDB Studio Agent builder and keep name: articles_qa_agent.
CREATE AGENT articles_qa_agent
USING
  model = 'gpt-4o-mini',
  prompt_template = 'You are an analyst for a news articles database. Answer using factual data from available tables.',
  tools = ['sql'];

-- Example ask:
-- SELECT answer FROM mindsdb.articles_qa_agent WHERE question = 'How many articles are from TechDaily?';
