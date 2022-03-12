from bs4 import BeautifulSoup
from app.main.model.model import MovimentacaoProcesso, MovimentacaoProcesso


def format_unidade_destino(unidade_destino):
    if not unidade_destino.strip():
        return "Unidade de destino não informado"
    else:
        return unidade_destino


def get_processos(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Procurando a tabela com as movimentações dos processos da PRAPE
    table_name = "Movimentações do Processo"
    for caption in soup.find_all('caption'):
        if caption.get_text() == table_name:
            table = caption.find_parent('table')
            break

    # Uma vez achado, pega todos os table rows da tabela
    movimentacoes = table.find_all('tr')

    # Aqui é pego o último table data da lista, correspondente a última movimentação
    ultima_movimentacao = movimentacoes[len(movimentacoes) - 1].find_all('td')
    ultima_movimentacao_copy = []
    
    for moma in ultima_movimentacao:

        # Caso tenha um despacho, é pego a penúltima movimentação que contém os dados necessários
        if 'Despacho Informativo' in moma.text:
            ultima_movimentacao_copy =  movimentacoes[len(movimentacoes) - 3].find_all('td')
            break

    if ultima_movimentacao_copy:
        ultima_movimentacao = ultima_movimentacao_copy

    unidade_destino = format_unidade_destino(ultima_movimentacao[2].text)
    recebido_em = ultima_movimentacao[4].text
    status_terminado = "PRA - ARQUIVO DA DAF" in unidade_destino

    return MovimentacaoProcesso(unidade_destino, recebido_em, status_terminado, url)
