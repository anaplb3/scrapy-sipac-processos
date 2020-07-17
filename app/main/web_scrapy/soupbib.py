from bs4 import BeautifulSoup
from app.main.model.model import MovimentacaoProcesso, MovimentacaoProcesso


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
    ultima_movimentacao_td = []

    ultima_movimentacao_td.extend(
        i.prettify() for i in movimentacoes[len(movimentacoes) - 1].find_all('td'))

    despacho = '<td nowrap="nowrap" width="10%">\n <a href="/public/jsp/processos/despacho_processo.jsf?idDespacho=264388">\n  <img alt="Visualizar Despacho" border="0" src="/sipac/img_css/geral/lupa.gif" title="Visualizar Despacho"/>\n </a>\n</td>\n'

    # Aqui é verificado se a última movimentação é um despacho, o que não é relevante para o sistema. Logo, é obtido a penúltima movimentação
    try:
        if ultima_movimentacao_td.index(despacho) > 0:
            ultima_movimentacao_td.clear()
            ultima_movimentacao_td.extend(
                i.prettify() for i in movimentacoes[len(movimentacoes) - 3].find_all('td'))
    except:
        pass

    unidade_destino = ultima_movimentacao_td[2].replace(
        "<td>", "").replace("\n", "").replace("</td>", "")
    recebido_em = ultima_movimentacao_td[4].replace(
        "<td>", "").replace("\n", "").replace("</td>", "")
    status_terminado = "PRA - ARQUIVO DA DAF" in unidade_destino

    return MovimentacaoProcesso(unidade_destino, recebido_em, status_terminado, url)
