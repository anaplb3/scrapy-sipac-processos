from bs4 import BeautifulSoup
from app.main.model.model import MovimentacaoProcesso


def get_processos(content):
    soup = BeautifulSoup(content, 'html.parser')

    table_name = "Movimentações do Processo"
    for caption in soup.find_all('caption'):
        if caption.get_text() == table_name:
            table = caption.find_parent('table')
            break

    movimentacoes = table.find_all('tr')
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

    json_objects = []
    for mov_obj in movimentacoes2:
        json_objects.append(mov_obj.serialize())

    return movimentacoes2
