import tkinter as tk
from tkinter import Scrollbar, INSERT
import random
import spacy
import difflib
from nltk.chat.util import Chat, reflections
from unidecode import unidecode

nlp = spacy.load("pt_core_news_sm")

def normalize(text):
    return unidecode(text).lower()

def fuzzy_match(input_text, patterns):
    best_score = 0
    best_responses = ["Desculpe, não entendi. Pode reformular a pergunta?"]

    for pattern, response in patterns:
        similarity = difflib.SequenceMatcher(None, input_text, pattern).ratio()
        if similarity > best_score:
            best_score = similarity
            best_responses = [random.choice(response)]
        elif similarity == best_score:
            best_responses.append(random.choice(response))

    return random.choice(best_responses)

pares = [
    [
        r"oi|olá",
        ["Oi! Como posso ajudar você?", "Olá! Qual é a sua pergunta?", "Olá! Estou aqui para ajudar."],
    ],
    [
        r"que tipos de tênis vocês têm?|me mostre os tênis|quais são os modelos disponíveis?",
        ["Temos uma grande variedade de tênis, incluindo tênis esportivos, casuais e de corrida. Como posso ajudar você a escolher?", "Nossos tênis incluem esportivos, casuais e de corrida. Qual é o seu estilo?"],
    ],
    [
        r"tipos de modelos",
        ["Temos uma grande variedade de tênis, incluindo tênis esportivos, casuais e de corrida. Como posso ajudar você a escolher?", "Nossos tênis incluem esportivos, casuais e de corrida. Qual é o seu estilo?"],
    ],
    [
        r"tenis colorido da nike",
        ["Temos uma variedade de tênis coloridos da Nike disponíveis."],
    ],
    [
        r"lancamentos",
        ["Para acessar os lancamentos entre na aba Lancamentos"],
    ],
    [
        r"adeus|até logo",
        ["Até logo! Se tiver mais alguma pergunta, é só perguntar.", "Tchau! Tenha um ótimo dia."],
    ],
    [
        r"estou com problemas|problema no pedido",
        ["Me diga, qual o seu problema?"],
    ],
    [
        r"Meu pedido foi cancelado devido a falta de estoque",
        ["Ocorreu um erro em nosso sistema onde seu pedido foi confirmado e não tinha mais esse produto em estoque, nesse caso te reembolsaremos o valor em 7 dias úteis."],
    ],
    [
        r"Meu pedido ainda não emitiu nota fiscal",
        ["No nosso sistema o pagamento ainda não foi aprovado, temos o prazo de 3 dias úteis para confirmar o pagamento e faturar o pedido."],
    ],
    [
        r"nota fiscal",
        ["No nosso sistema o pagamento ainda não foi aprovado, temos o prazo de 3 dias úteis para confirmar o pagamento e faturar o pedido."],
    ],
    [
        r"Cancelei meu pedido mas ainda não recebi o reembolso|reembolso|estorno|estornar|reembolsar",
        ["Temos o prazo de 7 dias úteis para confirmar o estorno, após a confirmação o valor estornado demora até 60 dias para aparecer na fatura de seu cartão."],
    ],
    [
        r"reembolso",
        ["Temos o prazo de 7 dias úteis para confirmar o estorno, após a confirmação o valor estornado demora até 60 dias para aparecer na fatura de seu cartão."],
    ],
    [
        r"Gostaria de trocar o meu pedido",
        ["Apos receber seu pedido voce tem o prazo de 30 dias para realizar a troca, acesse a aba pedidos, selecione o item que quer trocar e siga o passo a passo de acordo com o solicitado."],
    ],
    [
        r"trocar",
        ["Apos receber seu pedido voce tem o prazo de 30 dias para realizar a troca, acesse a aba pedidos, selecione o item que quer trocar e siga o passo a passo de acordo com o solicitado."],
    ],
    [
        r"Gostaria de devolver o meu pedido",
        ["Apos receber seu pedido voce tem o prazo de 30 dias para realizar a devoluçao, acesse a aba pedidos, selecione a opçao de devolver e siga o passo a passo de acordo com o solicitado.."],
    ],
    [
        r"Quero comprar um tênis|estou procurando tênis",
        ["Você procura por um tênis masculino ou feminino?"],
    ],
    [
        r"originais",
        ["Sim, nossos tenis sao originais e autenticados"],
    ],
    [
        r"Masculino",
        ["Temos diversas opções de tênis masculinos, diga para mim qual o estilo de tênis que você procura: casual, esportivo, social, ortopédico."],
    ],
    [
        r"Feminino",
        ["Temos diversas opções de tênis femininos, diga para mim qual o estilo de tênis que você procura: casual, esportivo, social, ortopédico."],
    ],
    [
        r"casual",
        ["De acordo com o que você procura te recomento o tênis Nike Air Jordan 1 Low, mas voce pode ver mais modelos em nosso site na aba 'Casuais'"],
    ],
    [
        r"tenis social",
        ["De acordo com o que você procura te recomento o tênis da marca Osklen, mas voce pode ver mais modelos em nosso site na aba 'Sociais'"],
    ],
    [
        r"esportivo",
        ["De acordo com o que você procura te recomento o tênis Adidas UltraBoost, mas voce pode ver mais modelos em nosso site na aba 'Esportivos'"],
    ],
    [
        r"ortopedico",
        ["De acordo com o que você procura te recomento o tênis da marca Skechers, mas voce pode ver mais modelos em nosso site na aba 'Ortopedicos'"],
    ],
    [
        r"Quais são as opções de entrega disponíveis?",
        ["Oferecemos entrega via PAC e Sedex. Confira o prazo de entrega durante o checkout do produto"],
    ],
    [
        r"prazo de entrega",
        ["Oferecemos entrega padrão, que leva de 3 a 5 dias úteis, e entrega expressa para entrega mais rápida em 1 a 2 dias úteis."],
    ],
    [
        r"entrega",
        ["Oferecemos entrega padrão, que leva de 3 a 5 dias úteis, e entrega expressa para entrega mais rápida em 1 a 2 dias úteis."],
    ],
    [
        r"como funciona a entrega",
        ["Oferecemos entrega padrão, que leva de 3 a 5 dias úteis, e entrega expressa para entrega mais rápida em 1 a 2 dias úteis."],
    ],
    [
        r"Como faço para rastrear meu pedido?",
        ["Para rastrear seu pedido, basta inserir o número de rastreamento na página 'Rastrear Pedido' em nosso site. Você receberá atualizações em tempo real sobre o status da entrega."],
    ],
    [
        r"rastrear",
        ["Para rastrear seu pedido, basta inserir o número de rastreamento na página 'Rastrear Pedido' em nosso site. Você receberá atualizações em tempo real sobre o status da entrega."],
    ],
    [
        r"Como faço para acompanhar o status do meu pedido?",
        ["Você pode acompanhar o status do seu pedido diretamente na sua conta no nosso site. Lá, você encontrará informações atualizadas sobre o envio e a entrega do seu pedido. Você também receberá todas as atualizações do seu pedido via e-mail."],
    ],
    [
        r"acompanhar",
        ["Você pode acompanhar o status do seu pedido diretamente na sua conta no nosso site. Lá, você encontrará informações atualizadas sobre o envio e a entrega do seu pedido. Você também receberá todas as atualizações do seu pedido via e-mail."],
    ],
    [
        r"status",
        ["Você pode acompanhar o status do seu pedido diretamente na sua conta no nosso site. Lá, você encontrará informações atualizadas sobre o envio e a entrega do seu pedido. Você também receberá todas as atualizações do seu pedido via e-mail."],
    ],
    [
        r"Qual é o tênis mais popular da sua loja?",
        ["Nossos tênis mais populares variam ao longo do tempo, mas atualmente, os modelos Nike Air Jordan e Nike Dunk são os favoritos entre nossos clientes. Você pode verificar no filtro de Mais Vendidos."],
    ],
    [
        r"Como posso verificar o tamanho certo para meus tênis?",
        ["É importante escolher o tamanho certo para obter o melhor ajuste. Você pode usar nossa guia de tamanhos no site para ajudá-lo a encontrar a medida correta. Além disso, você pode medir o comprimento do seu pé e compará-lo com nossas diretrizes de tamanho."],
    ],
    [
        r"Quais são as formas de pagamento aceitas?",
        ["Aceitamos pagamento com cartão de crédito, boleto bancário e Pix. Você pode escolher a opção de pagamento durante o processo de checkout no nosso site."],
    ],
    [
        r"pagamento",
        ["Aceitamos pagamento com cartão de crédito, boleto bancário e Pix. Você pode escolher a opção de pagamento durante o processo de checkout no nosso site."],
    ],
    [
        r"Quais são as tendências de tênis deste ano?",
        ["As tendências deste ano incluem tênis com design minimalista, cores vibrantes e modelos retrô. Posso mostrar alguns dos nossos tênis mais populares deste ano, se quiser."],
    ],
    [
        r"tendencias",
        ["As tendências deste ano incluem tênis com design minimalista, cores vibrantes e modelos retrô. Posso mostrar alguns dos nossos tênis mais populares deste ano, se quiser."],
    ],
    [
        r"Vocês têm tênis ecológicos?",
        ["Sim, estamos comprometidos com a sustentabilidade. Temos uma linha de tênis feitos com materiais reciclados e sustentáveis. Next nature *******."],
    ],
    [
        r"Quanto tempo leva para processar meu pedido?",
        ["Normalmente, levamos de 1 a 2 dias úteis para processar pedidos. Depois disso, o tempo de entrega depende da sua localização e da opção de envio escolhida. Você pode verificar o status do seu pedido na sua conta."],
    ],
    [
        r"processar",
        ["Normalmente, levamos de 1 a 2 dias úteis para processar pedidos. Depois disso, o tempo de entrega depende da sua localização e da opção de envio escolhida. Você pode verificar o status do seu pedido na sua conta."],
    ],
    [
        r"Como faço para escolher o tamanho certo para crianças?",
        ["Escolher o tamanho certo para crianças pode ser fácil. Você pode usar nossa guia de tamanhos no site, ou medir o pé da criança e seguir nossas diretrizes. Se tiver alguma dúvida, estamos aqui para ajudar!"],
    ],
    [
        r"Vocês têm tênis de edição limitada?",
        ["Sim, temos tênis de edição limitada de tempos em tempos. Esses modelos exclusivos são muito populares. Fique de olho no nosso site ou inscreva-se na nossa newsletter para receber atualizações sobre lançamentos de edição limitada."],
    ],
    [
        r"limitada?",
        ["Sim, temos tênis de edição limitada de tempos em tempos. Esses modelos exclusivos são muito populares. Fique de olho no nosso site ou inscreva-se na nossa newsletter para receber atualizações sobre lançamentos de edição limitada."],
    ],
    [
        r"desconto",
        ["Os tênis da nossa loja nao possuem descontos pois os valores sao tabelados de acordo com o fornecedor de cada marca."],
    ],
    [
        r"Existe um programa de afiliados para promover os produtos da sua loja?",
        ["Sim, temos um programa de afiliados. Você pode se inscrever no nosso site para se tornar um afiliado e ganhar comissões ao promover nossos produtos."],
    ],
    [
        r"Quais são as vantagens de comprar online em vez de ir até uma loja física?",
        ["Comprar online oferece conveniência, uma ampla seleção de produtos e a capacidade de comparar preços facilmente. Além disso, você pode aproveitar promoções exclusivas. No entanto, em lojas físicas, você pode experimentar os tênis antes de comprar."],
    ],
    [
        r"comprar online",
        ["Comprar online oferece conveniência, uma ampla seleção de produtos e a capacidade de comparar preços facilmente. Além disso, você pode aproveitar promoções exclusivas. No entanto, em lojas físicas, você pode experimentar os tênis antes de comprar."],
    ],
    [
        r"defeito",
        ["Nossa política de troca em caso de defeito é simples. Se o seu tênis apresentar qualquer defeito de fabricação, podemos trocá-lo por um novo dentro do período de garantia. Entre em contato conosco para iniciar o processo de troca."],
    ],
    [
        r"Como posso saber se um tênis está em promoção?",
        ["Você pode verificar as promoções na nossa página inicial ou na seção 'Ofertas Especiais' do nosso site. Além disso, assinantes da nossa newsletter recebem atualizações regulares sobre ofertas."],
    ],
    [
        r"Como faço para cancelar um pedido que acabei de fazer?",
        ["Para cancelar um pedido recente, entre em contato conosco o mais rápido possível pelo chat ao vivo ou telefone. Vamos ajudá-lo a cancelar o pedido, desde que ele ainda não tenha sido processado para envio."],
    ],
    [
        r"cancelar meu pedido",
        ["Para cancelar um pedido recente, entre em contato conosco o mais rápido possível pelo chat ao vivo ou telefone. Vamos ajudá-lo a cancelar o pedido, desde que ele ainda não tenha sido processado para envio."],
    ],
    [
        r"Vocês têm tênis de edição especial para colecionadores?",
        ["Sim, ocasionalmente lançamos tênis de edição especial para colecionadores. Esses modelos exclusivos são altamente valorizados por entusiastas. Fique de olho nas nossas redes sociais para informações sobre lançamentos de edição especial."],
    ],
    [
        r"Vocês têm tênis com materiais sustentáveis?",
        ["Sim, temos uma linha de tênis sustentáveis feitos com materiais reciclados e ecológicos. Eles são ideais para quem se preocupa com o meio ambiente. Quer ver nossas opções sustentáveis?"],
    ],
    [
        r"Como faço para cuidar dos meus tênis de couro?",
        ["Cuidar de tênis de couro é importante. Recomendamos limpar com um pano úmido e usar produtos de cuidado de couro. Evite deixá-los expostos ao sol direto e água em excesso para manter o couro em bom estado."],
    ],
    [
        r"Quais são as tendências de cores para tênis neste ano?",
        ["As tendências de cores para tênis deste ano incluem tons pastel, cores vivas e neutras versáteis. Você também encontrará tênis em cores metálicas. Quer ver algumas opções de tênis nas tendências atuais?"],
    ],
    [
        r"Vocês têm tênis de cano alto?",
        ["Sim, temos tênis de cano alto que oferecem suporte extra para os tornozelos. Eles são ótimos para estilo e funcionalidade. Quer ver nossos modelos de cano alto?"],
    ],
    [
        r"Posso fazer uma pré-encomenda de um tênis que ainda não foi lançado?",
        ["Sim, você pode fazer uma pré-encomenda de tênis que ainda não foram lançados. Entre em contato conosco para obter informações sobre como fazer uma pré-encomenda."],
    ],
    [
        r"Quanto tempo leva para que meu pedido seja entregue após a compra?",
        ["O tempo de entrega depende da sua localização e da opção de envio escolhida. Normalmente, leva de 3 a 5 dias úteis após o processamento do pedido. Você pode verificar o status do seu pedido na sua conta."],
    ],
    [
        r"Vocês oferecem garantia de satisfação?",
        ["Sim, temos uma garantia de satisfação. Se você não ficar satisfeito com seu tênis, você pode devolvê-lo dentro de 30 dias para um reembolso ou troca. Estamos comprometidos com a sua satisfação."],
    ],
    [
        r"Existe alguma taxa de devolução?",
        ["Não cobramos taxas de devolução, desde que o produto esteja dentro do prazo de nossa política de devolução e atenda aos requisitos de devolução. Você pode encontrar mais informações sobre nossa política de devolução no nosso site."],
    ],
    [
        r"Quais são os modelos mais indicados para quem pratica caminhada?",
        ["Para caminhada, recomendamos tênis de caminhada específicos, que oferecem conforto e suporte durante longas caminhadas. Nossos modelos da linha 'Walk Comfort' são ideais. Gostaria de ver as opções disponíveis?"],
    ],
    [
        r"Como faço para acompanhar o status da minha encomenda?",
        ["Você pode acompanhar o status da sua encomenda na sua conta no nosso site. Lá você encontrará informações atualizadas sobre o andamento da entrega do seu pedido."],
    ],
    [
        r"Vocês oferecem algum tipo de garantia de durabilidade para os tênis?",
        ["Sim, oferecemos garantia de durabilidade para nossos tênis. Eles são projetados para resistir ao desgaste normal e durar muito tempo. Se você tiver algum problema, nossa equipe de atendimento ao cliente está aqui para ajudar."],
    ],
    [
        r"Vocês fazem entrega internacional?",
        ["Sim, fazemos entregas internacionais para vários países. Você pode selecionar o país de destino durante o processo de compra para calcular os custos de envio."],
    ],
    [
        r"Quais são os tênis mais versáteis que vocês têm?",
        ["Nossos tênis mais versáteis são da linha 'All Terrain'. Eles são adequados para uma variedade de atividades, incluindo corrida, caminhada e treinamento. Gostaria de ver as opções disponíveis?"],
    ], 
]

pares_normalizados = [(normalize(pattern), response) for pattern, response in pares]

def chatbot_response(user_input):
    user_input_normalized = normalize(user_input)

    if user_input_normalized in ["adeus", "até logo"]:
        return "Até logo! Se tiver mais alguma pergunta, é só perguntar."

    best_response = fuzzy_match(user_input_normalized, pares_normalizados)
    return best_response

def enviar_pergunta():
    user_input = entrada.get()
    resposta = chatbot_response(user_input)

    historico.config(state="normal")
    historico.insert(tk.END, "Você: " + user_input + "\n", "usuario")
    historico.insert(tk.END, "Nico: " + resposta + "\n", "chatbot")
    historico.see(tk.END)  

    historico.tag_configure("usuario", foreground="black", justify='right', background='#FFCCFF')
    historico.tag_configure("chatbot", foreground="white", background='#4F2F4F')
    historico.config(state="disabled")
    entrada.delete(0, tk.END)

janela = tk.Tk()
janela.title("Chatbot Nico")
janela.geometry("400x600")  
janela.configure(bg="#FFCCFF")  

historico = tk.Text(janela, state="disabled", bg="#f0f0f0", wrap='word', font=('Segoe UI Black', 12))
historico.pack(expand=True, fill='both', padx=10, pady=10)

scrollbar = Scrollbar(janela, command=historico.yview)
scrollbar.pack(side='right')

historico['yscrollcommand'] = scrollbar.set

entrada = tk.Entry(janela, font=('Arial', 12), bg="white", relief="flat")
entrada.pack(expand=True, fill='x', pady=10, padx=10)

botao_enviar = tk.Button(janela, text="Enviar", command=enviar_pergunta, bg="#CC33CC", fg="white", font=('Segoe UI Black', 12))
botao_enviar.pack()

janela.mainloop()