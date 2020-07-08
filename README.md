# scrapy-sipac-processos
API que extrai os dados dos auxílios da UFPB para fins de acompanhamento. Atualmente estão disponíveis os Campus I, II, III, IV e os auxílios:

 - Moradia ("auxilio_moradia")
 - Alimentação ("auxilio_alimentacao")
 - Alimentação residência ("auxilio_alimentacao_res")
 - Auxílio emergencial COVID19 ("auxilio_emergencial")

# Response
Os dados estão disponíveis na url [https://consultaprocessosipac.herokuapp.com/processos](https://consultaprocessosipac.herokuapp.com/processos). Para o GET é necessário enviar um json no seguinte formato:

    {
    
    "auxilio": "auxilio_emergencial",
    
    "campus": "IV"
    
    }
o que retorna um array com cada movimentação do processo em questão:

    {
    
	    "data": [
    
	    {
    
		    "atualizado_em": "Wed, 08 Jul 2020 15:47:35 GMT",
		    
		    "campus": "IV",
		    
		    "data_origem": " 04/06/2020 17:38",
		    
		    "recebido_em": " 04/06/2020 18:50",
		    
		    "tipo_auxilio": "auxilio_emergencial",
		    
		    "unidade_destino": " PRAPE - COORDENAÇÃO DE ASSISTÊNCIA E PROMOÇÃO ESTUDANTIS (COAPE) (11.00.63.01)",
		    
		    "unidade_origem": " PRÓ-REITORIA DE ASSISTÊNCIA E PROMOÇÃO AO ESTUDANTE (PRAPE) (11.00.63)"
    
	    },
    
	    {
    
		    "atualizado_em": "Wed, 08 Jul 2020 15:47:35 GMT",
		    
		    "campus": "IV",
		    
		    "data_origem": " 05/06/2020 17:51",
		    
		    "recebido_em": " 05/06/2020 22:19",
		    
		    "tipo_auxilio": "auxilio_emergencial",
		    
		    "unidade_destino": " PRÓ-REITORIA DE ADMINISTRAÇÃO (PRA) (11.00.47)",
		    
		    "unidade_origem": " PRAPE - COORDENAÇÃO DE ASSISTÊNCIA E PROMOÇÃO ESTUDANTIS (COAPE) (11.00.63.01)"
		    
	    },
	    {

		    "atualizado_em": "Wed, 08 Jul 2020 15:47:35 GMT",
		    
		    "campus": "IV",
		    
		    "data_origem": " 07/07/2020 13:25",
		    
		    "recebido_em": "",
		    
		    "tipo_auxilio": "auxilio_emergencial",
		    
		    "unidade_destino": " PRA - ARQUIVO DA DAF (11.01.08.01.02.02)",
		    
		    "unidade_origem": " PRA - DIVISÃO DE ADMINISTRAÇÃO E FINANÇAS (11.01.08.01.02)"
    
	    }
    
		]
    
    }
	    
      
Como a API ainda está em desenvolvimento haverá mudanças.
     
