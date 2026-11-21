import time
import random
import statistics
import json
import os
import sys
import importlib.util

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

spec_base = importlib.util.spec_from_file_location("erp_base_mod", os.path.join(BASE_DIR, "versao_base", "main.py"))
erp_base = importlib.util.module_from_spec(spec_base)
spec_base.loader.exec_module(erp_base)

spec_otim = importlib.util.spec_from_file_location("erp_otim_mod", os.path.join(BASE_DIR, "versao_otimizada", "main.py"))
erp_otim = importlib.util.module_from_spec(spec_otim)
spec_otim.loader.exec_module(erp_otim)


def gerar_massa_dados(n, cenario, semente=42):
    random.seed(semente)
    if cenario == "ordenado":
        ids = list(range(1, n + 1))
    elif cenario == "invertido":
        ids = list(range(n, 0, -1))
    else:
        ids = list(range(1, n + 1))
        random.shuffle(ids)

    produtos = []
    for i, id_val in enumerate(ids):
        preco = round(random.uniform(5.0, 500.0), 2)
        estoque = random.randint(0, 100)
        minimo = random.randint(5, 20)
        p = erp_otim.Produto(id_val, f"Produto {id_val}", "Geral", preco, estoque, minimo)
        produtos.append(p)
    return produtos


def medir_insercao_base(produtos_input):
    lista_prods = []
    comps = 0
    t0 = time.perf_counter()
    for novo_prod in produtos_input:
        pos_inserir = len(lista_prods)
        for i in range(len(lista_prods)):
            comps += 1
            if lista_prods[i].id > novo_prod.id:
                pos_inserir = i
                break
        lista_prods.insert(pos_inserir, novo_prod)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, comps, lista_prods


def medir_insercao_otimizada(produtos_input):
    arvore = erp_otim.ArvoreAVL()
    t0 = time.perf_counter()
    for novo_prod in produtos_input:
        arvore.inserir(novo_prod)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, arvore


def medir_busca_base(lista_prods, ids_procurar):
    t0 = time.perf_counter()
    comps = 0
    encontrados = 0
    for id_val in ids_procurar:
        inicio = 0
        fim = len(lista_prods) - 1
        achou = False
        while inicio <= fim:
            comps += 1
            meio = (inicio + fim) // 2
            if lista_prods[meio].id == id_val:
                achou = True
                encontrados += 1
                break
            elif lista_prods[meio].id < id_val:
                inicio = meio + 1
            else:
                fim = meio - 1
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, comps, encontrados


def medir_busca_otimizada(arvore, ids_procurar):
    t0 = time.perf_counter()
    comps = 0
    encontrados = 0
    for id_val in ids_procurar:
        atual = arvore.raiz
        while atual is not None:
            comps += 1
            if id_val == atual.id:
                encontrados += 1
                break
            elif id_val < atual.id:
                atual = atual.esquerda
            else:
                atual = atual.direita
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, comps, encontrados


def medir_remocao_base(lista_prods, ids_remover):
    copia = list(lista_prods)
    t0 = time.perf_counter()
    comps = 0
    for id_val in ids_remover:
        inicio = 0
        fim = len(copia) - 1
        pos = -1
        while inicio <= fim:
            comps += 1
            meio = (inicio + fim) // 2
            if copia[meio].id == id_val:
                pos = meio
                break
            elif copia[meio].id < id_val:
                inicio = meio + 1
            else:
                fim = meio - 1
        if pos != -1:
            copia.pop(pos)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, comps


def medir_remocao_otimizada(arvore, ids_remover):
    t0 = time.perf_counter()
    for id_val in ids_remover:
        arvore.remover(id_val)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0


def medir_ordenacao_insertion(produtos_input):
    t0 = time.perf_counter()
    erp_base.insertion_sort(produtos_input)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0


def medir_ordenacao_merge(produtos_input):
    t0 = time.perf_counter()
    erp_otim.merge_sort(produtos_input)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0


def medir_fila_base(pedidos):
    fila = erp_base.FilaPrioridade()
    t0 = time.perf_counter()
    for p in pedidos:
        fila.enfileirar(p)
    while not fila.esta_vazia():
        fila.desenfileirar()
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0


def medir_fila_otimizada(pedidos):
    fila = erp_otim.FilaPrioridade()
    t0 = time.perf_counter()
    for p in pedidos:
        fila.enfileirar(p)
    while not fila.esta_vazia():
        fila.desenfileirar()
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0


def executar_bateria_completa():
    volumes = [100, 1000, 10000]
    cenarios = ["aleatorio", "ordenado", "invertido"]
    repeticoes = 5

    resultados = {
        "metadados": {
            "linguagem": f"Python {sys.version.split()[0]}",
            "sistema_operacional": sys.platform,
            "repeticoes": repeticoes,
            "semente": 42
        },
        "experimentos": []
    }

    print("=" * 70)
    print("INICIANDO BENCHMARK COMPARATIVO CIENTIFICO (PARTE 1 vs PARTE 2)")
    print("=" * 70)

    for n in volumes:
        print(f"\n>>> EXECUTANDO TESTES PARA N = {n} REGISTROS <<<")

        for cenario in cenarios:
            tempos_ins_base = []
            tempos_ins_otim = []
            comps_ins_base = []

            for r in range(repeticoes):
                dados = gerar_massa_dados(n, cenario, semente=42 + r)
                t_b, c_b, l_b = medir_insercao_base(dados)
                t_o, arv = medir_insercao_otimizada(dados)
                tempos_ins_base.append(t_b)
                tempos_ins_otim.append(t_o)
                comps_ins_base.append(c_b)

            m_tb, s_tb = statistics.mean(tempos_ins_base), statistics.stdev(tempos_ins_base) if repeticoes > 1 else 0
            m_to, s_to = statistics.mean(tempos_ins_otim), statistics.stdev(tempos_ins_otim) if repeticoes > 1 else 0
            ganho = m_tb / m_to if m_to > 0 else 0
            var_pct = ((m_tb - m_to) / m_tb) * 100.0 if m_tb > 0 else 0

            resultados["experimentos"].append({
                "operacao": "Inserção",
                "cenario": cenario,
                "n": n,
                "tempo_base_ms": round(m_tb, 4),
                "desvio_base_ms": round(s_tb, 4),
                "tempo_otim_ms": round(m_to, 4),
                "desvio_otim_ms": round(s_to, 4),
                "ganho_x": round(ganho, 2),
                "variacao_pct": round(var_pct, 2)
            })

            print(f"Insercao [{cenario:9s}] N={n:5d} | Base: {m_tb:8.3f} ms | Otim: {m_to:8.3f} ms | Ganho: {ganho:6.2f}x | Var: {var_pct:6.2f}%")

        random.seed(42)
        dados_base = gerar_massa_dados(n, "aleatorio", semente=42)
        _, _, lista_base = medir_insercao_base(dados_base)
        _, arvore_otim = medir_insercao_otimizada(dados_base)

        ids_existentes = [p.id for p in random.sample(dados_base, min(n, 100))]
        ids_inexistentes = [n + 1000 + i for i in range(min(n, 100))]

        t_bb_ex, t_bo_ex = [], []
        t_bb_in, t_bo_in = [], []
        c_bb_ex, c_bo_ex = 0, 0
        c_bb_in, c_bo_in = 0, 0

        for r in range(repeticoes):
            tb, cb, _ = medir_busca_base(lista_base, ids_existentes)
            to, co, _ = medir_busca_otimizada(arvore_otim, ids_existentes)
            t_bb_ex.append(tb)
            t_bo_ex.append(to)
            c_bb_ex = cb
            c_bo_ex = co

            tb_in, cb_in, _ = medir_busca_base(lista_base, ids_inexistentes)
            to_in, co_in, _ = medir_busca_otimizada(arvore_otim, ids_inexistentes)
            t_bb_in.append(tb_in)
            t_bo_in.append(to_in)
            c_bb_in = cb_in
            c_bo_in = co_in

        m_tb_ex = statistics.mean(t_bb_ex)
        m_to_ex = statistics.mean(t_bo_ex)
        g_ex = m_tb_ex / m_to_ex if m_to_ex > 0 else 0
        v_ex = ((m_tb_ex - m_to_ex) / m_tb_ex) * 100.0 if m_tb_ex > 0 else 0

        m_tb_in = statistics.mean(t_bb_in)
        m_to_in = statistics.mean(t_bo_in)
        g_in = m_tb_in / m_to_in if m_to_in > 0 else 0
        v_in = ((m_tb_in - m_to_in) / m_tb_in) * 100.0 if m_tb_in > 0 else 0

        resultados["experimentos"].append({
            "operacao": "Busca (existente)",
            "cenario": "aleatorio",
            "n": n,
            "tempo_base_ms": round(m_tb_ex, 4),
            "tempo_otim_ms": round(m_to_ex, 4),
            "comps_base": c_bb_ex,
            "comps_otim": c_bo_ex,
            "ganho_x": round(g_ex, 2),
            "variacao_pct": round(v_ex, 2)
        })

        resultados["experimentos"].append({
            "operacao": "Busca (inexistente)",
            "cenario": "aleatorio",
            "n": n,
            "tempo_base_ms": round(m_tb_in, 4),
            "tempo_otim_ms": round(m_to_in, 4),
            "comps_base": c_bb_in,
            "comps_otim": c_bo_in,
            "ganho_x": round(g_in, 2),
            "variacao_pct": round(v_in, 2)
        })

        print(f"Busca Existente      N={n:5d} | Base: {m_tb_ex:8.4f} ms | Otim: {m_to_ex:8.4f} ms | Ganho: {g_ex:6.2f}x | Comps Base: {c_bb_ex} vs Otim: {c_bo_ex}")
        print(f"Busca Inexistente    N={n:5d} | Base: {m_tb_in:8.4f} ms | Otim: {m_to_in:8.4f} ms | Ganho: {g_in:6.2f}x | Comps Base: {c_bb_in} vs Otim: {c_bo_in}")

        ids_rem = ids_existentes[:min(len(ids_existentes), 50)]
        t_rem_b, t_rem_o = [], []
        for r in range(repeticoes):
            tb, _ = medir_remocao_base(lista_base, ids_rem)
            to = medir_remocao_otimizada(arvore_otim, ids_rem)
            t_rem_b.append(tb)
            t_rem_o.append(to)
            _, arvore_otim = medir_insercao_otimizada(dados_base)

        m_tr_b = statistics.mean(t_rem_b)
        m_tr_o = statistics.mean(t_rem_o)
        g_rem = m_tr_b / m_tr_o if m_tr_o > 0 else 0
        v_rem = ((m_tr_b - m_tr_o) / m_tr_b) * 100.0 if m_tr_b > 0 else 0

        resultados["experimentos"].append({
            "operacao": "Remoção",
            "cenario": "aleatorio",
            "n": n,
            "tempo_base_ms": round(m_tr_b, 4),
            "tempo_otim_ms": round(m_tr_o, 4),
            "ganho_x": round(g_rem, 2),
            "variacao_pct": round(v_rem, 2)
        })
        print(f"Remocao              N={n:5d} | Base: {m_tr_b:8.4f} ms | Otim: {m_tr_o:8.4f} ms | Ganho: {g_rem:6.2f}x")

        t_sort_b, t_sort_o = [], []
        for r in range(repeticoes):
            dados_sort = gerar_massa_dados(n, "aleatorio", semente=100 + r)
            tb = medir_ordenacao_insertion(dados_sort)
            to = medir_ordenacao_merge(dados_sort)
            t_sort_b.append(tb)
            t_sort_o.append(to)

        m_sb = statistics.mean(t_sort_b)
        m_so = statistics.mean(t_sort_o)
        g_sort = m_sb / m_so if m_so > 0 else 0
        v_sort = ((m_sb - m_so) / m_sb) * 100.0 if m_sb > 0 else 0

        resultados["experimentos"].append({
            "operacao": "Ordenação Relatório",
            "cenario": "aleatorio",
            "n": n,
            "tempo_base_ms": round(m_sb, 4),
            "tempo_otim_ms": round(m_so, 4),
            "ganho_x": round(g_sort, 2),
            "variacao_pct": round(v_sort, 2)
        })
        print(f"Ordenacao (Sort)     N={n:5d} | Base: {m_sb:8.3f} ms | Otim: {m_so:8.3f} ms | Ganho: {g_sort:6.2f}x | Var: {v_sort:6.2f}%")

        pedidos = []
        for i in range(n):
            u = 1 if i % 3 == 0 else 2
            pedidos.append(erp_otim.PedidoReposicao(i + 1, f"P {i+1}", 10, u))

        t_fila_b, t_fila_o = [], []
        for r in range(repeticoes):
            tb = medir_fila_base(pedidos)
            to = medir_fila_otimizada(pedidos)
            t_fila_b.append(tb)
            t_fila_o.append(to)

        m_fb = statistics.mean(t_fila_b)
        m_fo = statistics.mean(t_fila_o)
        g_fila = m_fb / m_fo if m_fo > 0 else 0
        v_fila = ((m_fb - m_fo) / m_fb) * 100.0 if m_fb > 0 else 0

        resultados["experimentos"].append({
            "operacao": "Fila Prioridade (Heap)",
            "cenario": "misto",
            "n": n,
            "tempo_base_ms": round(m_fb, 4),
            "tempo_otim_ms": round(m_fo, 4),
            "ganho_x": round(g_fila, 2),
            "variacao_pct": round(v_fila, 2)
        })
        print(f"Fila Prioridade      N={n:5d} | Base: {m_fb:8.3f} ms | Otim: {m_fo:8.3f} ms | Ganho: {g_fila:6.2f}x | Var: {v_fila:6.2f}%")

    out_file = os.path.join(os.path.dirname(__file__), "resultados_benchmark.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"BENCHMARK CONCLUIDO COM SUCESSO! Resultados salvos em: {out_file}")
    print("=" * 70)


if __name__ == "__main__":
    executar_bateria_completa()
