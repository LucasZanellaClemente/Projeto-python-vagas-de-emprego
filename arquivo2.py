import requests
import json
import csv
from googletrans import Translator
import datetime

# Inicializa o tradutor
tradutor = Translator()

# Entrada do usuário
area = input(" Para area de tecnologia\nInsira a área que deseja procurar:\n  ")
lugar = input("de onde você é ....")

if area != "":
    # Traduz o termo de busca para inglês (para a API entender melhor)
    resultado = tradutor.translate(area, src="pt", dest="en")
    print(f"\n🔍 Buscando vagas para: '{resultado.text}'...\n")

    # Configuração da API
    API_KEY = "fe195371e4c2cb5bdae6cb82c7be3a49e3615e2b"
    url = "https://findwork.dev/api/jobs/"

    params = {
        "search": resultado.text,
        "location":lugar

    }
    headers = {"Authorization": f"Token {API_KEY}"}
    try:
        # Faz a requisição
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()

    except:
        pass

    # Verifica se há resultados
    if not data.get("results"):
        print("⚠️ Nenhuma vaga encontrada.")
    else:
        vagas_traduzidas = []  # lista para salvar os dados

        for job in data["results"]:
            print("="*80)
            print(f"📌 Título: {job['role']}")
            print(f"🏢 Empresa: {job['company_name']}")
            print(f"📍 Local: {job['location']}")
            print(f"🔗 Link: {job['url']}")
            
            print("-"*80)

            # Tradução da descrição da vaga para português
            descricao_en = job.get("text", "")
            if len(descricao_en) > 4500:
                descricao_en = descricao_en[:4500]
            traducao = tradutor.translate(descricao_en, src="en", dest="pt")
            descricao_pt = traducao.text
            
            print("📝 Descrição traduzida:")
            print(descricao_pt[:100] + "...")
            print("="*80, "\n")

            # Salva na lista para exportar depois
            vagas_traduzidas.append([
                job["role"],
                job["company_name"],
                job["location"],
                job["url"],
                descricao_pt
            ])

            # Salva os dados em um arquivo CSV
            nome_arquivo = f"vagas_.json"
            # with open(nome_arquivo, "w", newline="", encoding="utf-8") as file:
            #     writer = json.writer(file)
            #     writer.writerow(["Título", "Empresa", "Local", "Link", "Descrição (PT)"])
            #     writer.writerows(vagas_traduzidas)

            # print(f"✅ Arquivo '{nome_arquivo}' salvo com sucesso ({len(vagas_traduzidas)} vagas).")
            with open(f"vagas-{area}.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        print("✅ Dados salvos em vagas.json")
else:
    print("programa encerrado sem nenhuma busca feita")