# scrapy-sipac-processos
API que extrai os dados dos auxílios da UFPB para fins de acompanhamento. Atualmente estão disponíveis os Campus I, MANGABEIRA, II, III, IV, e os auxílios:

 - Moradia ("auxilio_moradia")
 - Alimentação ("auxilio_alimentacao")
 - Alimentação residência ("auxilio_alimentacao_residencia")
 - Auxílio emergencial COVID19 ("auxilio_emergencial")
 - Auxílio emergencial complementar COVID19 ("auxilio_emergencial_complementar")
 - Residência RUMF ("auxilio_residencia_rumf")
 - Residência RUFET ("auxilio_residencia_rufet")
 - Alimentação residentes Mangabeira e Santa Rita ("auxilio_residentes")
 

# Response
Os dados estão disponíveis para visualização [aqui](https://consultaprocessosipac.herokuapp.com/api/v1/docs). Para o GET é necessário enviar na url os parâmetros no formato abaixo:

    
    /processos?auxilio={id_auxilio}&campus={id_campus}
    
o que retorna um objeto com os seguintes atributos:

    {
    "response": {
        "body": {
            "atualizado_em": "Sat, 08 Aug 2020 19:05:00 GMT",
            "campus": "IV",
            "link_processo": "https://sipac.ufpb.br/public/jsp/processos/processo_detalhado.jsf?id=1888044",
            "mes_referente": "Agosto/2020",
            "proxima_atualizacao_em": "Sat, 08 Aug 2020 19:35:00 GMT",
            "recebido_em": "",
            "status_terminado": false,
            "tipo_auxilio": "auxilio_emergencial",
            "unidade_destino": " PRA - COORDENAÇÃO DE ADMINISTRAÇÃO (11.01.08.02)"
        },
        "code": "200",
        "message": "Auxílio encontrado com sucesso."
    }
    }
	    
      
Como a API ainda está em desenvolvimento haverá mudanças.
     
