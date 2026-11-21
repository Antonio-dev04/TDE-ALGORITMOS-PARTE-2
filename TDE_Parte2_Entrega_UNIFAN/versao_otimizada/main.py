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


class NodeAVL:
    def __init__(self, produto):
        self.produto = produto
        self.id = produto.id
        self.altura = 1
        self.esquerda = None
        self.direita = None


class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self._tamanho = 0

    def altura(self, no):
        if no is None:
            return 0
        return no.altura

    def fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def atualizar_altura(self, no):
        no.altura = 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def rotacao_direita(self, y):
        x = y.esquerda
        t2 = x.direita
        x.direita = y
        y.esquerda = t2
        self.atualizar_altura(y)
        self.atualizar_altura(x)
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        t2 = y.esquerda
        y.esquerda = x
        x.direita = t2
        self.atualizar_altura(x)
        self.atualizar_altura(y)
        return y

    def _inserir(self, no, produto):
        if no is None:
            self._tamanho += 1
            return NodeAVL(produto)

        if produto.id < no.id:
            no.esquerda = self._inserir(no.esquerda, produto)
        elif produto.id > no.id:
            no.direita = self._inserir(no.direita, produto)
        else:
            return no

        self.atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        if fb > 1 and produto.id < no.esquerda.id:
            return self.rotacao_direita(no)

        if fb < -1 and produto.id > no.direita.id:
            return self.rotacao_esquerda(no)

        if fb > 1 and produto.id > no.esquerda.id:
            no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)

        if fb < -1 and produto.id < no.direita.id:
            no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)

        return no

    def inserir(self, produto):
        if self.buscar(produto.id) is not None:
            return False
        self.raiz = self._inserir(self.raiz, produto)
        return True

    def buscar(self, id_procurado):
        atual = self.raiz
        while atual is not None:
            if id_procurado == atual.id:
                return atual.produto
            elif id_procurado < atual.id:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def _menor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _remover(self, no, id_procurado):
        if no is None:
            return None

        if id_procurado < no.id:
            no.esquerda = self._remover(no.esquerda, id_procurado)
        elif id_procurado > no.id:
            no.direita = self._remover(no.direita, id_procurado)
        else:
            if no.esquerda is None:
                self._tamanho -= 1
                return no.direita
            elif no.direita is None:
                self._tamanho -= 1
                return no.esquerda

            sucessor = self._menor_no(no.direita)
            no.produto = sucessor.produto
            no.id = sucessor.id
            no.direita = self._remover(no.direita, sucessor.id)

        if no is None:
            return None

        self.atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        if fb > 1 and self.fator_balanceamento(no.esquerda) >= 0:
            return self.rotacao_direita(no)

        if fb > 1 and self.fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)

        if fb < -1 and self.fator_balanceamento(no.direita) <= 0:
            return self.rotacao_esquerda(no)

        if fb < -1 and self.fator_balanceamento(no.direita) > 0:
            no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)

        return no

    def remover(self, id_procurado):
        prod = self.buscar(id_procurado)
        if prod is None:
            return None
        self.raiz = self._remover(self.raiz, id_procurado)
        return prod

    def em_ordem(self):
        resultado = []
        def _percorrer(no):
            if no is not None:
                _percorrer(no.esquerda)
                resultado.append(no.produto)
                _percorrer(no.direita)
        _percorrer(self.raiz)
        return resultado

    def pre_ordem(self):
        resultado = []
        def _percorrer(no):
            if no is not None:
                resultado.append(no.produto)
                _percorrer(no.esquerda)
                _percorrer(no.direita)
        _percorrer(self.raiz)
        return resultado

    def pos_ordem(self):
        resultado = []
        def _percorrer(no):
            if no is not None:
                _percorrer(no.esquerda)
                _percorrer(no.direita)
                resultado.append(no.produto)
        _percorrer(self.raiz)
        return resultado

    def tamanho(self):
        return self._tamanho

    def esta_vazia(self):
        return self.raiz is None


class FilaPrioridade:
    def __init__(self):
        self.itens = []
        self.contador = 0

    def enfileirar(self, pedido):
        entrada = [pedido.urgencia, self.contador, pedido]
        self.contador += 1
        self.itens.append(entrada)
        self._subir(len(self.itens) - 1)

    def _subir(self, i):
        while i > 0:
            pai = (i - 1) // 2
            if self.itens[i][0] < self.itens[pai][0] or (self.itens[i][0] == self.itens[pai][0] and self.itens[i][1] < self.itens[pai][1]):
                self.itens[i], self.itens[pai] = self.itens[pai], self.itens[i]
                i = pai
            else:
                break

    def desenfileirar(self):
        if len(self.itens) == 0:
            return None
        if len(self.itens) == 1:
            return self.itens.pop()[2]

        topo = self.itens[0][2]
        self.itens[0] = self.itens.pop()
        self._descer(0)
        return topo

    def _descer(self, i):
        tamanho = len(self.itens)
        while True:
            menor = i
            esq = 2 * i + 1
            dir = 2 * i + 2

            if esq < tamanho:
                if self.itens[esq][0] < self.itens[menor][0] or (self.itens[esq][0] == self.itens[menor][0] and self.itens[esq][1] < self.itens[menor][1]):
                    menor = esq

            if dir < tamanho:
                if self.itens[dir][0] < self.itens[menor][0] or (self.itens[dir][0] == self.itens[menor][0] and self.itens[dir][1] < self.itens[menor][1]):
                    menor = dir

            if menor != i:
                self.itens[i], self.itens[menor] = self.itens[menor], self.itens[i]
                i = menor
            else:
                break

    def esta_vazia(self):
        return len(self.itens) == 0

    def tamanho(self):
        return len(self.itens)

    def listar(self):
        copia = []
        for el in self.itens:
            copia.append([el[0], el[1], el[2]])

        ordenados = []
        while len(copia) > 0:
            menor_idx = 0
            for k in range(1, len(copia)):
                if copia[k][0] < copia[menor_idx][0] or (copia[k][0] == copia[menor_idx][0] and copia[k][1] < copia[menor_idx][1]):
                    menor_idx = k
            ordenados.append(copia.pop(menor_idx)[2])
        return ordenados


def merge_sort(lista):
    if len(lista) <= 1:
        copia = []
        for x in lista:
            copia.append(x)
        return copia

    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])

    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i].preco <= direita[j].preco:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado


produtos = ArvoreAVL()
fornecedores = []
pilha_movimentacoes = Pilha()
fila_reposicao = FilaPrioridade()


def carregar_dados():
    produtos.inserir(Produto(1, "Arroz 5kg", "Alimentos", 28.50, 4, 10))
    produtos.inserir(Produto(2, "Feijao 1kg", "Alimentos", 8.90, 0, 8))
    produtos.inserir(Produto(3, "Azeite 500ml", "Alimentos", 42.00, 15, 5))
    produtos.inserir(Produto(4, "Detergente 500ml", "Limpeza", 3.20, 25, 10))
    produtos.inserir(Produto(5, "Sabao em Po 1kg", "Limpeza", 14.50, 0, 6))

    fornecedores.append(Fornecedor(1, "Distribuidora Alianca", "(75) 3221-1000"))
    fornecedores.append(Fornecedor(2, "Quimica Nacional", "(75) 3222-2000"))

    fila_reposicao.enfileirar(PedidoReposicao(2, "Feijao 1kg", 20, 1))
    fila_reposicao.enfileirar(PedidoReposicao(1, "Arroz 5kg", 10, 2))


def cadastrar_produto():
    print("\n--- CADASTRAR PRODUTO ---")
    id_prod = int(input("ID do produto: "))

    achou = produtos.buscar(id_prod)
    if achou is not None:
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
    produtos.inserir(novo_prod)
    print("Produto cadastrado com sucesso na Arvore AVL!")


def consultar_produto():
    print("\n--- CONSULTAR PRODUTO (BUSCA EM ARVORE AVL) ---")
    id_prod = int(input("Digite o ID para buscar: "))
    prod = produtos.buscar(id_prod)

    if prod is not None:
        print("Produto encontrado na Arvore AVL:")
        print("Nome:", prod.nome)
        print("Categoria:", prod.categoria)
        print("Preco: R$", prod.preco)
        print("Estoque:", prod.estoque, "(Minimo:", prod.estoque_minimo, ")")
    else:
        print("Produto nao encontrado!")


def alterar_produto():
    print("\n--- ALTERAR PRODUTO ---")
    id_prod = int(input("ID do produto a alterar: "))
    prod = produtos.buscar(id_prod)

    if prod is None:
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
    removido = produtos.remover(id_prod)

    if removido is None:
        print("Produto nao encontrado!")
        return

    print("Produto", removido.nome, "removido com sucesso da Arvore AVL!")


def movimentar_estoque():
    print("\n--- MOVIMENTAR ESTOQUE ---")
    id_prod = int(input("ID do produto: "))
    prod = produtos.buscar(id_prod)

    if prod is None:
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
    if mov is None:
        print("A pilha esta vazia! Nenhuma acao para desfazer.")
        return

    prod = produtos.buscar(mov["id_produto"])
    if prod is None:
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
    print("\n--- REPOSICAO DE ESTOQUE (MIN-HEAP BINARIO) ---")
    print("1 - Fazer novo pedido de reposicao")
    print("2 - Atender pedido mais urgente da fila")
    print("3 - Ver fila de pedidos")
    op = input("Escolha: ")

    if op == "1":
        id_prod = int(input("ID do produto a repor: "))
        prod = produtos.buscar(id_prod)
        if prod is None:
            print("Produto nao encontrado!")
            return

        qtd = int(input("Quantidade a comprar: "))
        print("Urgencia: 1 - Urgente (estoque zerado) | 2 - Normal")
        urg = int(input("Urgencia (1 ou 2): "))
        if urg != 1:
            urg = 2

        novo_pedido = PedidoReposicao(prod.id, prod.nome, qtd, urg)
        fila_reposicao.enfileirar(novo_pedido)
        print("Pedido colocado na fila com sucesso via Min-Heap!")

    elif op == "2":
        pedido = fila_reposicao.desenfileirar()
        if pedido is None:
            print("Nenhum pedido pendente na fila!")
            return

        prod = produtos.buscar(pedido.id_produto)
        if prod is not None:
            prod.estoque = prod.estoque + pedido.quantidade
            print("Pedido atendido!")
            print("Foram adicionadas", pedido.quantidade, "unidades ao estoque de", prod.nome)
            print("Estoque atual:", prod.estoque)

    elif op == "3":
        print("\n=== FILA DE REPOSICAO (MIN-HEAP) ===")
        if fila_reposicao.esta_vazia():
            print("Fila vazia.")
        else:
            pedidos = fila_reposicao.listar()
            for i in range(len(pedidos)):
                p = pedidos[i]
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
    print("1 - Listar produtos (Travessias da Arvore AVL)")
    print("2 - Filtrar produtos por categoria")
    print("3 - Produtos com estoque baixo ou zerado")
    print("4 - Produtos ordenados por preco (Merge Sort manual)")
    print("5 - Ver historico de acoes na pilha")
    op = input("Escolha: ")

    if op == "1":
        print("\nEscolha o tipo de travessia da Arvore AVL:")
        print("1 - Em ordem (chaves crescentes de ID)")
        print("2 - Pre-ordem (hierarquia a partir da raiz)")
        print("3 - Pos-ordem (filhos antes do pai)")
        tipo_trav = input("Escolha (1, 2 ou 3): ")

        if tipo_trav == "1":
            lista = produtos.em_ordem()
            titulo = "TRAVESSIA EM ORDEM (ID CRESCENTE)"
        elif tipo_trav == "2":
            lista = produtos.pre_ordem()
            titulo = "TRAVESSIA PRE-ORDEM (RAIZ PRIMEIRO)"
        elif tipo_trav == "3":
            lista = produtos.pos_ordem()
            titulo = "TRAVESSIA POS-ORDEM (FILHOS PRIMEIRO)"
        else:
            lista = produtos.em_ordem()
            titulo = "TRAVESSIA EM ORDEM (PADRAO)"

        print(f"\n=== {titulo} ===")
        if len(lista) == 0:
            print("Nenhum produto cadastrado.")
        else:
            for p in lista:
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
        for p in produtos.em_ordem():
            if p.categoria.lower() == cat:
                print("ID:", p.id, "| Nome:", p.nome, "| Preco: R$", p.preco, "| Estoque:", p.estoque)
                achou = True
        if not achou:
            print("Nenhum produto encontrado nessa categoria.")

    elif op == "3":
        print("\n=== PRODUTOS COM ESTOQUE BAIXO OU ZERADO ===")
        for p in produtos.em_ordem():
            if p.estoque <= p.estoque_minimo:
                print("ID:", p.id, "| Nome:", p.nome, "| Estoque atual:", p.estoque, "| Minimo:", p.estoque_minimo)

    elif op == "4":
        print("\n=== PRODUTOS ORDENADOS POR MENOR PRECO (MERGE SORT) ===")
        todos = produtos.em_ordem()
        ordenados = merge_sort(todos)
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
        print("   SISTEMA ERP DE VAREJO - OTIMIZADO")
        print("=" * 45)
        print("1 - Cadastrar Produto (Arvore AVL)")
        print("2 - Consultar Produto por ID (Busca AVL)")
        print("3 - Alterar Produto")
        print("4 - Remover Produto (Remocao Balanceada)")
        print("5 - Movimentar Estoque (Entrada / Saida)")
        print("6 - Desfazer Ultima Acao (Pilha - LIFO)")
        print("7 - Reposicao de Estoque (Min-Heap)")
        print("8 - Fornecedores (CRUD)")
        print("9 - Relatorios (Travessias, Merge Sort)")
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
