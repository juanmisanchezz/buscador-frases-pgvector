from db import conectar, embedding, DIMENSIONES
conn = conectar()

conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
conn.execute("DROP TABLE IF EXISTS frases")
conn.execute(f"CREATE TABLE frases (id SERIAL PRIMARY KEY, tenant_id TEXT, texto TEXT, embedding VECTOR({DIMENSIONES}))")
conn.execute("CREATE INDEX ON frases USING hnsw (embedding vector_cosine_ops)")

