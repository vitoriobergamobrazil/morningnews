import json
import feedparser
from datetime import datetime
import pytz

def buscar_noticias_varejo():
    """Busca notícias e filtra como um 'sniper' apenas o que importa para o setor"""
    # Adicionamos mais fontes, incluindo foco em mercado e negócios
    urls_rss = [
        "https://www.infomoney.com.br/negocios/feed/",
        "https://exame.com/feed/",
        "https://valor.globo.com/rss/empresas"
    ]
    
    # O SEU RADAR: O robô só vai capturar a notícia se ela contiver alguma dessas palavras no título
    palavras_chave = [
        "varejo", "supermercado", "hipermercado", "atacarejo", 
        "aquisição", "fusões", "alimentos", "bebidas", "logística",
        "distribuição", "faturamento", "positivação", "ambev", "carrefour", "assaí", "atacado"
    ]
    
    noticias_selecionadas = []
    
    for url in urls_rss:
        feed = feedparser.parse(url)
        for entrada in feed.entries:
            titulo_min = entrada.title.lower()
            
            # Validação simples: Verifica se alguma palavra-chave está no título
            if any(palavra in titulo_min for palavra in palavras_chave):
                # Evita notícias duplicadas
                if not any(n['titulo'] == entrada.title for n in noticias_selecionadas):
                    noticias_selecionadas.append({
                        "titulo": entrada.title,
                        "link_aprofundar": entrada.link
                    })
            
            # Trava: Queremos as 4 melhores do dia, para não poluir o painel
            if len(noticias_selecionadas) >= 4:
                break
        if len(noticias_selecionadas) >= 4:
            break
                
    # Caso seja um domingo ou feriado e não haja movimentação no setor
    if not noticias_selecionadas:
        noticias_selecionadas.append({
            "titulo": "Radar limpo. Nenhuma movimentação de grande impacto no varejo alimentar e logística nas últimas horas.",
            "link_aprofundar": "#"
        })
        
    return noticias_selecionadas

def gerar_painel():
    noticias_de_hoje = buscar_noticias_varejo()
    
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_br).strftime("%d/%m/%Y %H:%M")

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

    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        
    print("Briefing matinal focado em varejo gerado com sucesso!")

if __name__ == "__main__":
    gerar_painel()
