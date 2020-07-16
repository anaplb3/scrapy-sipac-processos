from bs4 import BeautifulSoup
from app.main.model.model import MovimentacaoProcesso, MovimentacaoProcesso


def get_processos(html_content, url):
    print("url = {}".format(url))
    soup = BeautifulSoup(html_content, 'html.parser')

    table_name = "Movimentações do Processo"
    for caption in soup.find_all('caption'):
        if caption.get_text() == table_name:
            table = caption.find_parent('table')
            break

    movimentacoes = table.find_all('tr')
    ultima_movimentacao_td = []
    ultima_movimentacao_td.extend(
        i.prettify() for i in movimentacoes[len(movimentacoes) - 1].find_all('td'))

    unidade_destino = ultima_movimentacao_td[2].replace(
        "<td>", "").replace("\n", "").replace("</td>", "")
    recebido_em = ultima_movimentacao_td[4].replace(
        "<td>", "").replace("\n", "").replace("</td>", "")
    status_terminado = "PRA - ARQUIVO DA DAF" in unidade_destino

    print("unidade = {} \n recebido = {} \n status = {}".format(unidade_destino, recebido_em, status_terminado))

    return MovimentacaoProcesso(unidade_destino, recebido_em, status_terminado, url)

    """ movimentacoes[len(movimentacoes)].find_all('td').prettify()
    td = []
    for mov in movimentacoes:
        if not mov:
            continue
        else:
            td_list = []
            td_list.extend(i.prettify() for i in mov.find_all('td'))
            td.append(td_list)

    movimentacoes2 = []

    for mov2 in td:
        if len(mov2) != 7:
            continue
        else:
            dataOrigem = mov2[0].replace(
                "<td>", "").replace("\n", "").replace("</td>", "")
            unidade_origem = mov2[1].replace(
                "<td>", "").replace("\n", "").replace("</td>", "")
            unidade_destino = mov2[2].replace(
                "<td>", "").replace("\n", "").replace("</td>", "")
            enviado_por = mov2[3].replace(
                "<td>", "").replace("\n", "").replace("</td>", "")
            recebido_em = mov2[4].replace(
                "<td>", "").replace("\n", "").replace("</td>", "")
            recebido_por = mov2[5].replace(
                "<td>", "").replace("\n", "").replace("</td>", "")
            urgente = mov2[6].replace("<td>", "").replace("\n", "").replace(
                "</td>", "").replace("", '').replace('<td style="text-align: center;">', "")
            movimentacoes2.append(
                MovimentacaoProcesso(
                    dataOrigem, unidade_origem, unidade_destino, enviado_por, recebido_em, recebido_por, urgente)
            )

    return movimentacoes2 """
