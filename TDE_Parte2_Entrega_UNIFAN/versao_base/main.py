class Produto:
    def __init__(self, id, nome, categoria, preco, estoque, estoque_minimo):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque
        self.estoque_minimo = estoque_minimo


class Fornecedor:
    def __init__(self, id, nome, telefone):
        self.id = id
        self.nome = nome
        self.telefone = telefone


class PedidoReposicao:
    def __init__(self, id_produto, nome_produto, quantidade, urgencia):
        self.id_produto = id_produto
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.urgencia = urgencia


class Pilha:
    def __init__(self):
        self.itens = []

    def push(self, item):
        self.itens.append(item)

    def pop(self):
        if len(self.itens) == 0:
            return None
        return self.itens.pop()

    def esta_vazia(self):
        return len(self.itens) == 0


class FilaPrioridade:
    def __init__(self):
        self.itens = []

    def enfileirar(self, pedido):
        posicao = len(self.itens)
        for i in range(len(self.itens)):
            if pedido.urgencia < self.itens[i].urgencia:
                posicao = i
                break
        self.itens.insert(posicao, pedido)

    def desenfileirar(self):
        if len(self.itens) == 0:
            return None
        return self.itens.pop(0)

    def esta_vazia(self):
        return len(self.itens) == 0


def busca_binaria(id_procurado):
    inicio = 0
    fim = len(produtos) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if produtos[meio].id == id_procurado:
            return meio, produtos[meio]
        elif produtos[meio].id < id_procurado:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1, None


def insertion_sort(lista_original):
    copia = []
    for item in lista_original:
        copia.append(item)

    for i in range(1, len(copia)):
        pivo = copia[i]
        j = i - 1
        while j >= 0 and copia[j].preco > pivo.preco:
            copia[j + 1] = copia[j]
            j = j - 1
        copia[j + 1] = pivo

    return copia


produtos = []
fornecedores = []
pilha_movimentacoes = Pilha()
fila_reposicao = FilaPrioridade()


def carregar_dados():
    produtos.append(Produto(1, "Arroz 5kg", "Alimentos", 28.50, 4, 10))
    produtos.append(Produto(2, "Feijao 1kg", "Alimentos", 8.90, 0, 8))
    produtos.append(Produto(3, "Azeite 500ml", "Alimentos", 42.00, 15, 5))
    produtos.append(Produto(4, "Detergente 500ml", "Limpeza", 3.20, 25, 10))
    produtos.append(Produto(5, "Sabao em Po 1kg", "Limpeza", 14.50, 0, 6))

    fornecedores.append(Fornecedor(1, "Distribuidora Alianca", "(75) 3221-1000"))
    fornecedores.append(Fornecedor(2, "Quimica Nacional", "(75) 3222-2000"))

    fila_reposicao.enfileirar(PedidoReposicao(2, "Feijao 1kg", 20, 1))
    fila_reposicao.enfileirar(PedidoReposicao(1, "Arroz 5kg", 10, 2))


def cadastrar_produto():
    print("\n--- CADASTRAR PRODUTO ---")
    id_prod = int(input("ID do produto: "))

    pos, achou = busca_binaria(id_prod)
    if achou != None:
        print("Erro: Ja existe um produto com esse ID!")
        return

    nome = input("Nome do produto: ")
    if nome == "":
        print("Erro: Nome nao pode ser vazio!")
        return

    categoria = input("Categoria: ")
    preco = float(input("Preco: "))
    if preco <= 0:
        print("Erro: Preco deve ser maior que zero!")
        return

    estoque = int(input("Quantidade em estoque: "))
    estoque_minimo = int(input("Estoque minimo de seguranca: "))

    novo_prod = Produto(id_prod, nome, categoria, preco, estoque, estoque_minimo)
    pos_inserir = len(produtos)
    for i in range(len(produtos)):
        if produtos[i].id > novo_prod.id:
            pos_inserir = i
            break
    produtos.insert(pos_inserir, novo_prod)
    print("Produto cadastrado com sucesso!")


def consultar_produto():
    print("\n--- CONSULTAR PRODUTO (BUSCA BINARIA) ---")
    id_prod = int(input("Digite o ID para buscar: "))
    pos, prod = busca_binaria(id_prod)

    if prod != None:
        print("Produto encontrado na posicao", pos, "da lista:")
        print("Nome:", prod.nome)
        print("Categoria:", prod.categoria)
        print("Preco: R$", prod.preco)
        print("Estoque:", prod.estoque, "(Minimo:", prod.estoque_minimo, ")")
    else:
        print("Produto nao encontrado!")


def alterar_produto():
    print("\n--- ALTERAR PRODUTO ---")
    id_prod = int(input("ID do produto a alterar: "))
    pos, prod = busca_binaria(id_prod)

    if prod == None:
        print("Produto nao encontrado!")
        return

    print("Produto:", prod.nome, "| Preco atual: R$", prod.preco)
    novo_preco = float(input("Novo preco: "))
    novo_minimo = int(input("Novo estoque minimo: "))

    prod.preco = novo_preco
    prod.estoque_minimo = novo_minimo
    print("Produto atualizado com sucesso!")


def remover_produto():
    print("\n--- REMOVER PRODUTO ---")
    id_prod = int(input("ID do produto a remover: "))
    pos, prod = busca_binaria(id_prod)

    if prod == None:
        print("Produto nao encontrado!")
        return

    removido = produtos.pop(pos)
    print("Produto", removido.nome, "removido com sucesso!")


def movimentar_estoque():
    print("\n--- MOVIMENTAR ESTOQUE ---")
    id_prod = int(input("ID do produto: "))
    pos, prod = busca_binaria(id_prod)

    if prod == None:
        print("Produto nao encontrado!")
        return

    print("Produto:", prod.nome, "| Estoque atual:", prod.estoque)
    print("1 - Entrada no estoque")
    print("2 - Saida (Venda)")
    tipo_op = input("Escolha (1 ou 2): ")
    qtd = int(input("Quantidade: "))

    if qtd <= 0:
        print("Quantidade invalida!")
        return

    if tipo_op == "1":
        prod.estoque = prod.estoque + qtd
        tipo_texto = "ENTRADA"
        print("Entrada registrada! Novo estoque:", prod.estoque)
    elif tipo_op == "2":
        if prod.estoque < qtd:
            print("Erro: Estoque insuficiente! Saldo atual:", prod.estoque)
            return
        prod.estoque = prod.estoque - qtd
        tipo_texto = "SAIDA"
        print("Venda registrada! Novo estoque:", prod.estoque)
    else:
        print("Opcao invalida!")
        return

    movimento = {
        "id_produto": prod.id,
        "nome": prod.nome,
        "tipo": tipo_texto,
        "quantidade": qtd
    }
    pilha_movimentacoes.push(movimento)


def desfazer_acao():
    print("\n--- DESFAZER ULTIMA ACAO (PILHA - LIFO) ---")
    mov = pilha_movimentacoes.pop()
    if mov == None:
        print("A pilha esta vazia! Nenhuma acao para desfazer.")
        return

    pos, prod = busca_binaria(mov["id_produto"])
    if prod == None:
        print("O produto dessa acao nao existe mais.")
        return

    if mov["tipo"] == "ENTRADA":
        prod.estoque = prod.estoque - mov["quantidade"]
        print("Desfeito: foi retirado", mov["quantidade"], "do estoque de", prod.nome)
    else:
        prod.estoque = prod.estoque + mov["quantidade"]
        print("Desfeito: foi devolvido", mov["quantidade"], "ao estoque de", prod.nome)

    print("Estoque atual de", prod.nome, "agora e:", prod.estoque)


def reposicao_estoque():
    print("\n--- REPOSICAO DE ESTOQUE (FILA DE PRIORIDADE) ---")
    print("1 - Fazer novo pedido de reposicao")
    print("2 - Atender pedido mais urgente da fila")
    print("3 - Ver fila de pedidos")
    op = input("Escolha: ")

    if op == "1":
        id_prod = int(input("ID do produto a repor: "))
        pos, prod = busca_binaria(id_prod)
        if prod == None:
            print("Produto nao encontrado!")
            return

        qtd = int(input("Quantidade a comprar: "))
        print("Urgencia: 1 - Urgente (estoque zerado) | 2 - Normal")
        urg = int(input("Urgencia (1 ou 2): "))
        if urg != 1:
            urg = 2

        novo_pedido = PedidoReposicao(prod.id, prod.nome, qtd, urg)
        fila_reposicao.enfileirar(novo_pedido)
        print("Pedido colocado na fila com sucesso!")

    elif op == "2":
        pedido = fila_reposicao.desenfileirar()
        if pedido == None:
            print("Nenhum pedido pendente na fila!")
            return

        pos, prod = busca_binaria(pedido.id_produto)
        if prod != None:
            prod.estoque = prod.estoque + pedido.quantidade
            print("Pedido atendido!")
            print("Foram adicionadas", pedido.quantidade, "unidades ao estoque de", prod.nome)
            print("Estoque atual:", prod.estoque)

    elif op == "3":
        print("\n=== FILA DE REPOSICAO ===")
        if fila_reposicao.esta_vazia():
            print("Fila vazia.")
        else:
            for i in range(len(fila_reposicao.itens)):
                p = fila_reposicao.itens[i]
                if p.urgencia == 1:
                    urg_nome = "URGENTE (Estoque Zerado)"
                else:
                    urg_nome = "Normal"
                print(i + 1, "o da fila -> Produto:", p.nome_produto, "| Qtd:", p.quantidade, "| Urgencia:", urg_nome)


def crud_fornecedores():
    print("\n--- FORNECEDORES (CRUD COMPLETO) ---")
    print("1 - Cadastrar fornecedor")
    print("2 - Consultar fornecedor por ID")
    print("3 - Alterar telefone do fornecedor")
    print("4 - Remover fornecedor")
    print("5 - Listar todos os fornecedores")
    op = input("Escolha: ")

    if op == "1":
        id_f = int(input("ID do fornecedor: "))
        for f in fornecedores:
            if f.id == id_f:
                print("Erro: Ja existe fornecedor com esse ID!")
                return
        nome = input("Nome da empresa / Fornecedor: ")
        tel = input("Telefone: ")
        if nome != "" and tel != "":
            fornecedores.append(Fornecedor(id_f, nome, tel))
            print("Fornecedor cadastrado com sucesso!")
        else:
            print("Erro: Nome e telefone sao obrigatorios!")

    elif op == "2":
        id_f = int(input("Digite o ID do fornecedor: "))
        achou = False
        for f in fornecedores:
            if f.id == id_f:
                print("Fornecedor encontrado:")
                print("ID:", f.id, "| Nome:", f.nome, "| Tel:", f.telefone)
                achou = True
                break
        if not achou:
            print("Fornecedor nao encontrado.")

    elif op == "3":
        id_f = int(input("ID do fornecedor para alterar: "))
        achou = False
        for f in fornecedores:
            if f.id == id_f:
                print("Fornecedor:", f.nome, "| Telefone atual:", f.telefone)
                f.telefone = input("Novo telefone: ")
                print("Telefone atualizado com sucesso!")
                achou = True
                break
        if not achou:
            print("Fornecedor nao encontrado.")

    elif op == "4":
        id_f = int(input("ID do fornecedor a remover: "))
        for i in range(len(fornecedores)):
            if fornecedores[i].id == id_f:
                rem = fornecedores.pop(i)
                print("Fornecedor", rem.nome, "removido com sucesso!")
                return
        print("Fornecedor nao encontrado.")

    elif op == "5":
        print("\n=== LISTA DE FORNECEDORES ===")
        if len(fornecedores) == 0:
            print("Nenhum fornecedor cadastrado.")
        else:
            for f in fornecedores:
                print("ID:", f.id, "| Nome:", f.nome, "| Tel:", f.telefone)


def relatorios():
    print("\n--- RELATORIOS DO SISTEMA ---")
    print("1 - Listar todos os produtos")
    print("2 - Filtrar produtos por categoria")
    print("3 - Produtos com estoque baixo ou zerado")
    print("4 - Produtos ordenados por preco (Insertion Sort manual)")
    print("5 - Ver historico de acoes na pilha")
    op = input("Escolha: ")

    if op == "1":
        print("\n=== TODOS OS PRODUTOS ===")
        for p in produtos:
            if p.estoque == 0:
                status = "Zerado (Critico)"
            elif p.estoque < p.estoque_minimo:
                status = "Abaixo do Minimo"
            else:
                status = "Normal"
            print("ID:", p.id, "| Nome:", p.nome, "| Cat:", p.categoria, "| Preco: R$", p.preco, "| Estoque:", p.estoque, "(Min:", p.estoque_minimo, ") | Status:", status)

    elif op == "2":
        cat = input("Digite a categoria (ex: Alimentos, Limpeza): ").lower()
        print("\n=== PRODUTOS DA CATEGORIA", cat.upper(), "===")
        achou = False
        for p in produtos:
            if p.categoria.lower() == cat:
                print("ID:", p.id, "| Nome:", p.nome, "| Preco: R$", p.preco, "| Estoque:", p.estoque)
                achou = True
        if not achou:
            print("Nenhum produto encontrado nessa categoria.")

    elif op == "3":
        print("\n=== PRODUTOS COM ESTOQUE BAIXO OU ZERADO ===")
        for p in produtos:
            if p.estoque <= p.estoque_minimo:
                print("ID:", p.id, "| Nome:", p.nome, "| Estoque atual:", p.estoque, "| Minimo:", p.estoque_minimo)

    elif op == "4":
        print("\n=== PRODUTOS ORDENADOS POR MENOR PRECO (INSERTION SORT) ===")
        ordenados = insertion_sort(produtos)
        for p in ordenados:
            print("Preco: R$", p.preco, "| ID:", p.id, "| Nome:", p.nome, "| Estoque:", p.estoque)

    elif op == "5":
        print("\n=== HISTORICO NA PILHA (DO TOPO PARA A BASE) ===")
        if pilha_movimentacoes.esta_vazia():
            print("Pilha vazia.")
        else:
            for i in range(len(pilha_movimentacoes.itens) - 1, -1, -1):
                m = pilha_movimentacoes.itens[i]
                print("-> Tipo:", m["tipo"], "| Produto:", m["nome"], "| Qtd:", m["quantidade"])


def menu():
    carregar_dados()

    while True:
        print("\n" + "=====================================")
        print("      SISTEMA ERP DE VAREJO - UNIFAN")
        print("=" * 45)
        print("1 - Cadastrar Produto")
        print("2 - Consultar Produto por ID (Busca Binaria)")
        print("3 - Alterar Produto")
        print("4 - Remover Produto")
        print("5 - Movimentar Estoque (Entrada / Saida)")
        print("6 - Desfazer Ultima Acao (Pilha - LIFO)")
        print("7 - Reposicao de Estoque (Fila de Prioridade)")
        print("8 - Fornecedores (CRUD)")
        print("9 - Relatorios (Geral, Filtro, Ordenacao)")
        print("0 - Sair")
        print("=====================================")
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            consultar_produto()
        elif opcao == "3":
            alterar_produto()
        elif opcao == "4":
            remover_produto()
        elif opcao == "5":
            movimentar_estoque()
        elif opcao == "6":
            desfazer_acao()
        elif opcao == "7":
            reposicao_estoque()
        elif opcao == "8":
            crud_fornecedores()
        elif opcao == "9":
            relatorios()
        elif opcao == "0":
            print("\nEncerrando o programa. Bom trabalho!")
            break
        else:
            print("Opcao invalida! Digite de 0 a 9.")


if __name__ == "__main__":
    menu()
