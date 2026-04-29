import os
import json
import feedparser
import google.generativeai as genai
from datetime import datetime
import pytz

# Configuração da IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def buscar_noticias_brutas():
    urls_rss = [
        "https://www.infomoney.com.br/negocios/feed/",
        "https://exame.com/feed/",
        "https://valor.globo.com/rss/empresas"
    ]
    todas_noticias = []
    for url in urls_rss:
        feed = feedparser.parse(url)
        for entrada in feed.entries[:10]: # Pega as 10 últimas de cada fonte
            todas_noticias.append(f"Título: {entrada.title} | Link: {entrada.link}")
    return "\n".join(todas_noticias)

def processar_com_ia(texto_noticias):
    prompt = f"""
    Você é um Consultor Executivo de Inteligência para Vitório Bergamo Neto, Gerente Matricial Nacional de Varejo na Triunfante.
    Sua tarefa é filtrar e analisar as notícias abaixo:
    
    {texto_noticias}
    
    DIRETRIZES:
    1. Filtre apenas o que for relevante para: Varejo Alimentar, Supermercados, Atacarejo, Distribuição, Indústria de Bens de Consumo (Bebidas/Alimentos) e Fusões/Aquisições no Brasil.
    2. Ignore notícias de entretenimento, política pura ou curiosidades irrelevantes.
    3. Para cada notícia selecionada (máximo 4), forneça:
       - Um título executivo.
       - Um resumo de 3 tópicos focados em INSIGHTS ESTRATÉGICOS para a Triunfante.
       - O link original.
    4. Crie uma "Curiosidade do Dia" sobre gestão, história do comércio ou ciência que ajude no aprendizado contínuo.
    5. Selecione um "Versículo Bíblico" de Provérbios ou Salmos sobre liderança e sabedoria, com uma breve aplicação para o dia.

    RESPONDA EXATAMENTE NO FORMATO JSON ABAIXO:
    {{
      "noticias": [
        {{"titulo": "...", "resumo": "...", "link": "..."}}
      ],
      "curiosidade": "...",
      "sabedoria": {{"versiculo": "...", "texto": "..."}}
    }}
    """
    response = model.generate_content(prompt)
    return json.loads(response.text)

def gerar_painel():
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_br).strftime("%d/%m/%Y %H:%M")
    
    print("Buscando notícias...")
    noticias_brutas = buscar_noticias_brutas()
    
    print("Analisando com Gemini IA...")
    briefing_ia = processar_com_ia(noticias_brutas)
    
    dados = {
        "data_atualizacao": agora,
        "noticias": briefing_ia['noticias'],
        "agenda": [
            {"horario": "Foco", "compromisso": "Integrar API da Agenda do Google (Próxima etapa)"}
        ],
        "curiosidade": briefing_ia['curiosidade'],
        "sabedoria": briefing_ia['sabedoria']
    }

    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    print("Painel inteligente gerado com sucesso!")

if __name__ == "__main__":
    gerar_painel()
