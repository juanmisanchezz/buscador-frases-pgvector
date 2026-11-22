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

PREGUNTAS = [
    ("hotel_mar", "A que hora empieza el horario del desayuno?"),
    ("hotel_cielo", "A que hora empieza el horario del desayuno?"),
    ("hotel_cielo", "Donde puedo encontrar esquis?")
]

for hotel_cliente, pregunta in PREGUNTAS:
    Vector = embedding(pregunta)
    print()
    resultados = conn.execute("SELECT texto, embedding <=> %s FROM frases WHERE tenant_id = %s ORDER BY embedding <=> %s LIMIT 2", (Vector, hotel_cliente, Vector))
    print(hotel_cliente, pregunta)
    for texto, distancia in resultados:
        print (f"{1-distancia:.2f}| {texto}")

