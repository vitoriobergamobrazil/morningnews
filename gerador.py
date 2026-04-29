import json
import feedparser
from datetime import datetime
import pytz

def buscar_noticias_macro():
    """Busca as notícias reais do InfoMoney e Exame usando os Feeds oficiais"""
    urls_rss = [
        "https://www.infomoney.com.br/negocios/feed/",
        "https://exame.com/feed/"
    ]
    
    noticias_selecionadas = []
    
    for url in urls_rss:
        feed = feedparser.parse(url)
        # Pega as 2 notícias mais recentes de cada portal
        for entrada in feed.entries[:2]:
            noticias_selecionadas.append({
                "titulo": entrada.title,
                "link_aprofundar": entrada.link
            })
            
    return noticias_selecionadas

def gerar_painel():
    # 1. Puxa as notícias reais
    noticias_de_hoje = buscar_noticias_macro()
    
    # 2. Pega o horário atual (Fuso de São Paulo/Brasília)
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_br).strftime("%d/%m/%Y %H:%M")

    # 3. Monta a estrutura de dados (que no futuro terá a integração da agenda e IA para curiosidades)
    dados = {
        "data_atualizacao": agora,
        "noticias": noticias_de_hoje,
        "agenda": [
            {"horario": "Foco", "compromisso": "Integrar API da Agenda do Google (Próxima etapa)"}
        ],
        "curiosidade": "Você sabia? A gestão matricial moderna foi fortemente impulsionada pela NASA na década de 1960 para gerenciar o Projeto Apollo. Eles precisavam de especialistas técnicos respondendo tanto a gerentes de projeto quanto a chefes de departamento simultaneamente.",
        "sabedoria": {
            "versiculo": "Não havendo sábia direção, o povo cai, mas na multidão de conselheiros há segurança.",
            "texto": "Provérbios 11:14"
        }
    }

    # 4. Salva o arquivo dados.json automaticamente
    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        
    print("Briefing matinal gerado com sucesso!")

if __name__ == "__main__":
    gerar_painel()
