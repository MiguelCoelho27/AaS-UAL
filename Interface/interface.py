import requests
import getpass

id_user_online= None
user_online = ""
password_admin="123456789"


def get_float_input(prompt):
    """Solicita um número float ao usuário, repetindo até receber um valor válido."""
    while True:
        valor = input(prompt).strip()
        try:
            return float(valor)
        except ValueError:
            print("Valor inválido. Por favor, insira um número (ex: 10.50).")

def get_int_input(prompt):
    """Solicita um número inteiro ao usuário, repetindo até receber um valor válido."""
    while True:
        valor = input(prompt).strip()
        try:
            return int(valor)
        except ValueError:
            print("Valor inválido. Por favor, insira um número inteiro (ex: 10).")
            
            
def register_user():
    print("*** Registar Utilizador ***")
    nome = input("Digite o nome: ")
    email = input("Digite o email: ")
    password = input("Digite o password: ")
    #new_user = User(nome,email,password)
    data = {"name": nome, "email": email, "password":password}
    print(f"JSON: {data}")  
    response = requests.post("http://127.0.0.1:5003/users", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code==201:
        data=response.json()
        global id_user_online
        id_user_online = data["id"]
        global user_online
        user_online= data["name"]
        return
    

def listar_events():
    events = pegar_todos_eventos()
    if events == []:
        print("Não há eventos disponiveis")
        return 500
    else:
        print("""
              -------------------------******EVENTOS******------------------------
              """)
        for i in events:
            print(f"ID: {i['id']} - EVENTO: {i['name']} - DATA E HORA: {i['date_time']} - PREÇO: €{i['price']}")
            print(20*"-----")
        return 200
    
def listar_tickets(tickets):
    
    if tickets == []:
        print("Não há tickets disponiveis")
        return 500
    else:
        print("""
              -------------------------******TICKETS******------------------------
              """)
       
        for i in tickets:
            print(f"ID: {i['id']} - EVENTO_ID: {i['id_event']} - ORDEM_ID: {i['id_order']} - STATUS: {i['status']}")
            print(20*"-----")
        return 200
    
def listar_ordens(ordens):
    
    if ordens == []:
        print("Não há ordens disponiveis")
        return 500
    else:
        print("""
              -------------------------******ORDENS******------------------------
              """)
       
        for i in ordens:
            print(f"ID: {i['id']} - EVENTO_ID: {i['id_event']} - PAGAMENTO_ID: {i['id_payment']} - STATUS: {i['status']}")
            print(20*"-----")
        return 200

def login_user():
    print("*** Login Utilizador ***")
    email = input("Digite o email: ")
    password = getpass.getpass("Digite o password: ")
    data = {"email": email, "password":password}
    response = requests.get("http://127.0.0.1:5003/users/login", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    if response.status_code==200:
        data= response.json()
        global id_user_online
        id_user_online = data["id"]
        global user_online
        user_online= data["name"]
        return 200
    else:
        return 400




def register_event():
    print("*** Registar Evento ***")
    password = getpass.getpass("Digite a senha de admin: ")

    global password_admin
    if password == password_admin:
        nome = input("Digite o nome do evento: ")
        description = input("Digite a descrição do evento: ")

        # Usa as funções auxiliares para garantir entradas válidas
        preco = get_float_input("Digite o preço: ")
        vagas = get_int_input("Digite o total de vagas: ")

        date_time = input("Data e hora (Ex: YYYY-MM-dd 20:30:00): ")

        data = {
            "name": nome,
            "description": description,
            "price": preco,
            "vagas": vagas,
            "date_time": date_time
        }
        print(f"JSON Enviado: {data}")
        
        response = requests.post("http://127.0.0.1:5000/events", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
    else:
        print("Senha incorreta, tente novamente.")

    

def pegar_todos_eventos():
    try:
        response = requests.get("http://127.0.0.1:5000/events")

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            #print("Eventos retornados com sucesso:", response.json())
            return response.json()  # Retorna o conteúdo JSON
        else:
            print(f"Erro ao buscar eventos. Status code: {response.status_code}")
            return {"error": f"Erro ao buscar eventos. Código: {response.status_code}"}
    except Exception as e:
        print(f"Erro durante a requisição: {str(e)}")
        return {"error": f"Erro durante a requisição: {str(e)}"}

def ver_tickets():
    try:
        global id_user_online
        if id_user_online == None:
            codigo = login_user()
            if codigo == 400 or codigo == 404 or codigo == 401:
                return      
        user_id = id_user_online
        response = requests.get(f"http://127.0.0.1:5002/tyckets/user/{user_id}")

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            listar_tickets(response.json())
            
            return response.json()  # Retorna o conteúdo JSON
        else:
            print(f"Erro ao buscar tickets. Status code: {response.status_code} erro: {response.json()}")
            return {"error": f"Erro ao buscar tickets. Código: {response.status_code}"}
    except Exception as e:
        print(f"Erro durante a requisição: {str(e)}")
        return {"error": f"Erro durante a requisição: {str(e)}"}

def ver_ordens():
    try:
        global id_user_online
        if id_user_online == None:
            codigo = login_user()
            if codigo == 400 or codigo == 404 or codigo == 401:
                return      
        user_id = id_user_online
        response = requests.get(f"http://127.0.0.1:5004/orders/user/{user_id}")

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            listar_ordens(response.json())
            
            return response.json()  # Retorna o conteúdo JSON
        else:
            print(f"Erro ao buscar ordens. Status code: {response.status_code}")
            return {"error": f"Erro ao buscar ordens. Código: {response.status_code}"}
    except Exception as e:
        print(f"Erro durante a requisição: {str(e)}")
        return {"error": f"Erro durante a requisição: {str(e)}"}

def make_order():
    print("\n*** Fazer Pedido ***")
    global id_user_online
    if id_user_online == None:
        codigo = login_user()
        if codigo == 400 or codigo == 404 or codigo == 401:
            return      
    user_id = id_user_online
    events = listar_events()
    if events == 500:
        print("Falha ao listar os eventos!")
        return
    else:    
        id_evento = get_int_input("Digite o ID do evento: ")
        try:
            response = requests.get(f"http://127.0.0.1:5000/events/{id_evento}")
            if response.status_code == 200:
                data_evento= response.json()
                vagas = data_evento['vagas']
                print(f"""
                      
                      ***HÁ UM TOTAL DE {vagas} RESERVAS DISPONIVEL PARA ESSE EVENTO!***
                      
                      """)
            else:
                print(response.json())
                print(response.status_code)
                return
        except Exception as e:
            print(f"Erro: {e}. Tente novamente.")
            return make_order()     
        quantidade = get_int_input("Digite a quantidade de reservas que deseja: ")
        if quantidade <=0:
            print("****---Digite uma quantidade maior que que 0!----****")
            make_order()
    response = requests.post("http://127.0.0.1:5004/orders", json={"user_id": user_id, "id_event": id_evento, "quantidade": quantidade})
    print(response.json())
    if response.status_code == 201:
        id_order = response.json()['id']
        id_payment = response.json()['id_payment']
        print(id_order)
        resposta = input("Deseja realizar o pagamento agora? (Y/N): ")
        if resposta.upper() == "Y":
            make_payment(id_order,id_payment)
    else:
        return response.json()
    
def make_payment(id_order, id_payment):
    print("""
    **** Formas de Pagamento ****
    1- Cartão
    2- Mbway
    3- Transferência Bancária
    """)
    form_pay = input("Qual a forma de pagamento: ").strip()
    payment_methods = {
        "1": "Cartão",
        "2": "Mbway",
        "3": "Transferência Bancária"
    }
    
    if form_pay in payment_methods:
        form_pay_name = payment_methods[form_pay]
        try:
            url = f"http://127.0.0.1:5001/payments/{id_payment}"
            response = requests.put(url, json={"id_order": id_order, "form_pay": form_pay_name, "status":"PAGO"})
            
            # Verifica o status da resposta
            if response.status_code == 200:
                print("Pagamento atualizado com sucesso!")
                print(response.json())
            else:
                print(f"Erro na atualização do pagamento: {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao tentar conectar ao serviço de pagamentos: {e}")
    else:
        print("Entrada inválida. Tente novamente.")
        make_payment(id_order, id_payment)

if __name__ == "__main__":
    while True:
        print(f"""
              Olá, {user_online}""")
        opcao = get_int_input("""
                        **** MENU ****
                        1- Registar utilizador
                        2- Login
                        3- Fazer pedido
                        4- Ver Minhas Ordens
                        5- Ver Meus tickets
                        6- Ver Eventos
                        7- Registar Evento
                        8- Sair
                        Qual a opção?
        """)
        if opcao == 1:
            register_user()
        elif opcao == 2:
            login_user()
        elif opcao == 3:
            make_order()
        elif opcao == 4:
            ver_ordens()
        elif opcao == 5:
            ver_tickets()
        elif opcao == 6:
            listar_events()
        elif opcao == 7:
            register_event()
        elif opcao==8:
            print("Saindo.....")
            break
        else:
            print("Opção inválida. Tente novamente.")


