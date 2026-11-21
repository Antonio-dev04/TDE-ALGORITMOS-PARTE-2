# TDE Parte 2: Otimização de Algoritmos e Relatório Técnico
## UNIFAN - Centro Universitário Nobre (2026.2)
### Disciplina: Algoritmos e Estruturas de Dados

---

### Equipe de Desenvolvimento
- **Antonio Magalhães** (antonio.magalhaes@souunifan.net.br)
- **Eduardo Santos** (eduardo.santos@souunifan.net.br)
- **Willian Gabriel** (willian.gabriel@souunifan.net.br)
- **Conrrado Menezes** (conrrado.menezes@souunifan.net.br)

---

### Visão Geral do Projeto

Este projeto compreende a Parte 2 do Trabalho Discente Efetivo (TDE), consistindo na evolução, otimização e análise comparativa de desempenho de um Sistema de ERP para Varejo originalmente desenvolvido na Parte 1.

O trabalho contém duas versões completas do sistema:
1. **Versão Base (Parte 1 Congelada):** Cadastro principal em lista linear, busca binária sobre lista, ordenação por inserção (Insertion Sort O(n²)) e fila de prioridade com inserção linear O(n).
2. **Versão Otimizada (Parte 2):** Cadastro principal em Árvore AVL balanceada manualmente (com rotações simples e duplas, inserção, busca e remoção em O(log n)), 3 travessias da árvore (em ordem, pré-ordem e pós-ordem), ordenação por divisão e conquista (Merge Sort manual O(n log n)) e fila de prioridade com Min-Heap binário manual O(log n).

---

### Estrutura de Diretórios

```text
├── versao_base/
│   └── main.py                     # Sistema ERP original da Parte 1 (congelado)
├── versao_otimizada/
│   └── main.py                     # Sistema ERP otimizado da Parte 2 (AVL, Merge Sort, Min-Heap)
├── benchmark/
│   ├── benchmark.py                # Suíte de experimentos empíricos com semente fixa
│   ├── gerar_graficos.py           # Script gerador dos gráficos científicos de desempenho
│   └── resultados_benchmark.json   # Dados brutos medidos com médias e desvios padrão
├── relatorio/
│   ├── Relatorio_Tecnico_SBC_Parte2.pdf   # Relatório Técnico no Padrão SBC (10 páginas)
│   ├── Relatorio_Tecnico_SBC_Parte2.docx  # Versão editável Word no Padrão SBC
│   └── figuras/                    # Gráficos em alta resolução (Figuras 1, 2 e 3)
└── README.md
```

---

### Instruções de Execução

#### 1. Executar a Versão Base (Parte 1)
```bash
python3 versao_base/main.py
```

#### 2. Executar a Versão Otimizada (Parte 2)
```bash
python3 versao_otimizada/main.py
```

#### 3. Executar o Benchmark Científico Comparativo
```bash
python3 benchmark/benchmark.py
```
O benchmark testa automaticamente coleções de N = 100, N = 1.000 e N = 10.000 registros nos cenários aleatório, ordenado e inverso, com 5 repetições por medição, calculando médias, desvios padrão, fatores de ganho e salvando os resultados em `benchmark/resultados_benchmark.json`.

#### 4. Gerar os Gráficos Científicos
```bash
python3 benchmark/gerar_graficos.py
```

---

### Principais Resultados Alcançados

- **Ordenação de Relatórios por Preço:** O Merge Sort reduziu o tempo de execução com N = 10.000 de 732,62 ms para 7,53 ms, gerando um ganho de **97,35x** (variação de 98,97%).
- **Fila de Prioridade de Reposição:** O Min-Heap binário reduziu o ciclo de enfileiramento e atendimento com N = 10.000 de 594,81 ms para 18,98 ms, gerando um ganho de **31,33x** (variação de 96,81%).
- **Inserção em Massa:** A Árvore AVL superou a lista linear na inserção de dados ordenados com N = 10.000 de 1.015,28 ms para 30,20 ms, gerando um ganho de **33,62x** (variação de 97,03%).
- **Casos Sem Ganho Documentados:** Para coleções reduzidas (N = 100), a lista linear exibiu tempos inferiores devido à sobrecarga de instanciação de nós da árvore e rotinas de balanceamento em Python.
