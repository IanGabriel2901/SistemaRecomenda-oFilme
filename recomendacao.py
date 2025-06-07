# Sistema de Recomendação de Filmes
# ------------------------------------------------

filmes = [
    {"id": 1, "titulo": "Inception", "genero": ["Ficção Científica", "Ação"], "avaliacao": 8.8, "ano": 2010, "popularidade": 95},
    {"id": 2, "titulo": "The Shawshank Redemption", "genero": ["Drama"], "avaliacao": 9.3, "ano": 1994, "popularidade": 98},
    {"id": 3, "titulo": "Interstellar", "genero": ["Ficção Científica", "Aventura"], "avaliacao": 8.6, "ano": 2014, "popularidade": 94},
    {"id": 4, "titulo": "Pulp Fiction", "genero": ["Crime", "Drama"], "avaliacao": 8.9, "ano": 1994, "popularidade": 97},
    {"id": 5, "titulo": "The Dark Knight", "genero": ["Ação", "Crime", "Drama"], "avaliacao": 9.0, "ano": 2008, "popularidade": 99},
]

usuario = {
    "nome": "Ian",
    "historico": ["Inception", "Interstellar"],
    "generos_preferidos": ["Ficção Científica", "Ação"],
    "nota_minima": 8.5,
}

def buscar_por_titulo(titulo, lista_filmes):
    filmes_ordenados = sorted(lista_filmes, key=lambda x: x["titulo"])
    esquerda, direita = 0, len(filmes_ordenados) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        filme_meio = filmes_ordenados[meio]["titulo"]
        if filme_meio == titulo:
            return filmes_ordenados[meio]
        elif filme_meio < titulo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return None

def buscar_por_genero(genero, lista_filmes):
    return [filme for filme in lista_filmes if genero in filme["genero"]]

def ordenar_por_avaliacao(lista_filmes, crescente=True):
    if len(lista_filmes) <= 1:
        return lista_filmes
    pivot = lista_filmes[len(lista_filmes) // 2]["avaliacao"]
    menores = [filme for filme in lista_filmes if filme["avaliacao"] < pivot]
    iguais = [filme for filme in lista_filmes if filme["avaliacao"] == pivot]
    maiores = [filme for filme in lista_filmes if filme["avaliacao"] > pivot]
    if crescente:
        return ordenar_por_avaliacao(menores, crescente) + iguais + ordenar_por_avaliacao(maiores, crescente)
    else:
        return ordenar_por_avaliacao(maiores, crescente) + iguais + ordenar_por_avaliacao(menores, crescente)

def ordenar_por_popularidade(lista_filmes):
    if len(lista_filmes) <= 1:
        return lista_filmes
    meio = len(lista_filmes) // 2
    esquerda = ordenar_por_popularidade(lista_filmes[:meio])
    direita = ordenar_por_popularidade(lista_filmes[meio:])
    return merge(esquerda, direita)

def merge(esquerda, direita):
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i]["popularidade"] >= direita[j]["popularidade"]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado

def recomendar_filmes(usuario, lista_filmes):
    nao_assistidos = [filme for filme in lista_filmes if filme["titulo"] not in usuario["historico"]]
    recomendados = [
        filme for filme in nao_assistidos
        if any(genero in usuario["generos_preferidos"] for genero in filme["genero"])
        and filme["avaliacao"] >= usuario["nota_minima"]
    ]
    recomendados_ordenados = sorted(
        recomendados,
        key=lambda x: (x["popularidade"] * 0.6 + x["avaliacao"] * 0.4),
        reverse=True
    )
    return recomendados_ordenados

# Exemplo de uso
if __name__ == "__main__":
    print("=== Sistema de Recomendação de Filmes ===")
    filme = buscar_por_titulo("Inception", filmes)
    print(f"\nFilme encontrado: {filme['titulo']}")

    ficcao = buscar_por_genero("Ficção Científica", filmes)
    print("\nFilmes de Ficção Científica:")
    for f in ficcao:
        print(f["titulo"])

    recomendacoes = recomendar_filmes(usuario, filmes)
    print("\nRecomendações para Ian:")
    for idx, filme in enumerate(recomendacoes, 1):
        print(f"{idx}. {filme['titulo']} (Avaliação: {filme['avaliacao']}, Popularidade: {filme['popularidade']})")
