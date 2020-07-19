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

    
    /processos?auxilio=auxilio_moradia&campus=IV
    
o que retorna um objeto com os seguintes atributos:

    {
		"data": {
			"atualizado_em": "Mon, 13 Jul 2020 16:51:51 GMT",
			"campus": "IV",
			"link_processo": "https://sipac.ufpb.br/public/jsp/processos/processo_detalhado.jsf?id=1881839",
			"recebido_em": "",
			"status_terminado": true,
			"tipo_auxilio": "auxilio_moradia",
			"unidade_destino": " PRA - ARQUIVO DA DAF (11.01.08.01.02.02)"
		}
	}
	    
      
Como a API ainda está em desenvolvimento haverá mudanças.
     
