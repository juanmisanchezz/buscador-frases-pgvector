from db import conectar, embedding, DIMENSIONES
conn = conectar()

conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
conn.execute("DROP TABLE IF EXISTS frases")
conn.execute(f"CREATE TABLE frases (id SERIAL PRIMARY KEY, tenant_id TEXT, texto TEXT, embedding VECTOR({DIMENSIONES}))")
conn.execute("CREATE INDEX ON frases USING hnsw (embedding vector_cosine_ops)")

FRASES = [
    ("hotel_mar", "El desayuno se sirve de 7 a 10 en la terraza"),
    ("hotel_mar", "La piscina abre de 9 de la mañana a 8 de la tarde"),
    ("hotel_mar", "El parking cuesta 15 euros por noche"),
    ("hotel_cielo", "El desayuno es de 8 a 11 en el comedor"),
    ("hotel_cielo", "Alquilamos esquís y botas en la recepción")
]

for hotel, texto in FRASES:
    conn.execute("INSERT INTO frases (tenant_id, texto, embedding) VALUES (%s, %s, %s)",
    (hotel, texto, embedding(texto)))
