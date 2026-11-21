import os
import sys
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
)
import pypdf

RELATORIO_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(RELATORIO_DIR, "figuras")
PDF_PATH = os.path.join(RELATORIO_DIR, "Relatorio_Tecnico_SBC_Parte2.pdf")


def gerar_pdf(escala_fig=0.46, espaco_parag=2.8, leading_corpo=13.2):
    margem_sup = 3.5 * cm
    margem_inf = 2.5 * cm
    margem_esq = 3.0 * cm
    margem_dir = 3.0 * cm

    largura_util = A4[0] - margem_esq - margem_dir

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=margem_esq,
        rightMargin=margem_dir,
        topMargin=margem_sup,
        bottomMargin=margem_inf
    )

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "SBCTitulo",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=16,
        leading=19,
        alignment=1,
        spaceAfter=10
    )

    estilo_autores = ParagraphStyle(
        "SBCAutores",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=11.5,
        leading=14,
        alignment=1,
        spaceAfter=2
    )

    estilo_inst = ParagraphStyle(
        "SBCInst",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9.5,
        leading=12,
        alignment=1,
        spaceAfter=2
    )

    estilo_email = ParagraphStyle(
        "SBCEmail",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=12,
        alignment=1,
        spaceAfter=12
    )

    estilo_corpo = ParagraphStyle(
        "SBCCorpo",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11.5,
        leading=leading_corpo,
        alignment=4,
        spaceAfter=espaco_parag
    )

    estilo_secao = ParagraphStyle(
        "SBCSecao",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=12.5,
        leading=15,
        alignment=0,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    estilo_subsecao = ParagraphStyle(
        "SBCSubsecao",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=11.5,
        leading=14,
        alignment=0,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    estilo_legenda_tab = ParagraphStyle(
        "SBCLegendaTab",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=9,
        leading=11,
        alignment=1,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    estilo_legenda_fig = ParagraphStyle(
        "SBCLegendaFig",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=9,
        leading=11,
        alignment=1,
        spaceBefore=2,
        spaceAfter=8
    )

    estilo_cod = ParagraphStyle(
        "SBCCod",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=9.5,
        alignment=0,
        spaceBefore=2,
        spaceAfter=4
    )

    estilo_tab_cel = ParagraphStyle(
        "SBCTabCel",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=7.5,
        leading=9,
        alignment=0
    )

    estilo_tab_cel_c = ParagraphStyle(
        "SBCTabCelC",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=7.5,
        leading=9,
        alignment=1
    )

    estilo_tab_hdr = ParagraphStyle(
        "SBCTabHdr",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=8,
        leading=9.5,
        alignment=1
    )

    estilo_ref = ParagraphStyle(
        "SBCRef",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=12,
        alignment=0,
        spaceAfter=3
    )

    story = []

    story.append(Paragraph("Otimização de Estruturas de Dados e Algoritmos em um Sistema de ERP para Varejo: Análise Comparativa Teórico-Empírica", estilo_titulo))
    story.append(Paragraph("Antonio Magalhães, Eduardo Santos, Willian Gabriel, Conrrado Menezes", estilo_autores))
    story.append(Paragraph("Centro Universitário Nobre (UNIFAN) – Feira de Santana – BA – Brasil", estilo_inst))
    story.append(Paragraph("{antonio.magalhaes, eduardo.santos, willian.gabriel, conrrado.menezes}@souunifan.net.br", estilo_email))

    resumo_html = (
        "<b>Resumo.</b> <i>Este trabalho apresenta a evolução, otimização e avaliação comparativa de desempenho de um Sistema de "
        "Planejamento de Recursos Empresariais (ERP) voltado ao comércio varejista, originalmente construído "
        "com estruturas lineares. Com o objetivo de solucionar gargalos assintóticos decorrentes do crescimento do volume "
        "de dados, foram projetadas e implementadas manualmente estruturas hierárquicas e algoritmos avançados: uma Árvore "
        "AVL balanceada com rotações para indexação principal de produtos, travessias completas (em ordem, pré-ordem e pós-ordem), "
        "o algoritmo Merge Sort para ordenação por divisão e conquista e um Min-Heap binário para a fila de reposição prioritária. "
        "Testes controlados para N variando de 100 a 10.000 registros comprovaram ganhos expressivos na versão otimizada, destacando-se "
        "uma aceleração de até 97,35x na ordenação de relatórios, 33,62x na inserção de dados ordenados e 31,33x no atendimento da fila de reposição, "
        "validando as predições da complexidade assintótica Big O e identificando com rigor os trade-offs de memória e casos sem ganho.</i>"
    )
    story.append(Paragraph(resumo_html, estilo_corpo))

    abstract_html = (
        "<b>Abstract.</b> <i>This paper presents the evolution, optimization, and empirical performance evaluation of a Retail Enterprise "
        "Resource Planning (ERP) system originally developed using linear data structures. To address asymptotic bottlenecks "
        "caused by data scalability, advanced structures and algorithms were manually designed and implemented: a self-balancing "
        "AVL Tree with rotations for product indexing, complete tree traversals (in-order, pre-order, and post-order), Merge Sort "
        "for divide-and-conquer reporting, and a binary Min-Heap for priority replenishment queues. Controlled experiments across "
        "N ranging from 100 to 10,000 records demonstrated substantial performance improvements in the optimized version, achieving "
        "a speedup of up to 97.35x in report sorting, 33.62x in sorted insertion, and 31.33x in queue dispatching, fully validating "
        "theoretical Big O bounds while rigorously assessing memory overhead and edge-case trade-offs.</i>"
    )
    story.append(Paragraph(abstract_html, estilo_corpo))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Introdução", estilo_secao))
    story.append(Paragraph(
        "Sistemas de Planejamento de Recursos Empresariais (ERP) constituem a espinha dorsal operacional de organizações comerciais, "
        "integrando módulos críticos como cadastro de produtos, controle de fornecedores, movimentações de entrada e saída de estoque, "
        "reversão de transações e reposição automatizada de itens em níveis críticos. Na Parte 1 deste projeto, desenvolveu-se um ERP "
        "funcional fundamentado estritamente em estruturas de dados lineares e algoritmos básicos (listas contíguas, busca linear/binária simples "
        "e ordenação por inserção). Embora tal abordagem atenda satisfatoriamente a volumes restritos de dezenas de itens, a expansão "
        "do catálogo para milhares de registros impõe severos custos computacionais decorrentes da complexidade assintótica desfavorável.",
        estilo_corpo
    ))

    story.append(Paragraph(
        "A literatura científica clássica (Cormen et al., 2012; Sedgewick e Wayne, 2016) preconiza que a viabilidade temporal de sistemas "
        "reais depende diretamente da seleção adequada de estruturas de dados e de algoritmos assintoticamente eficientes. Em um ambiente "
        "de varejo concorrente, tempos de resposta elevados afetam diretamente a experiência do operador, aumentam o custo operacional de "
        "infraestrutura de processamento e reduzem a capacidade de escala da organização.",
        estilo_corpo
    ))

    story.append(Paragraph(
        "Diante desse desafio, o objetivo geral deste trabalho é refatorar e otimizar o núcleo algorítmico do ERP desenvolvido na Parte 1, "
        "substituindo estruturas lineares ineficientes por estruturas balanceadas e hierárquicas, e documentar os resultados por meio de um "
        "estudo comparativo rigoroso no padrão da Sociedade Brasileira de Computação (SBC). Como objetivos específicos verificáveis, estabelecem-se: "
        "(i) implementar manualmente uma Árvore AVL balanceada com suporte a inserção, busca em O(log n), remoção balanceada e rotações simples e duplas; "
        "(ii) desenvolver três rotinas de travessia na árvore (em ordem, pré-ordem e pós-ordem) para emissão de dados hierárquicos; "
        "(iii) implementar manualmente o algoritmo Merge Sort por divisão e conquista para ordenação de relatórios; "
        "(iv) implementar um Min-Heap binário para a fila de prioridades de reposição; "
        "(v) conduzir medições empíricas comparativas entre a versão base e a versão otimizada sob cenários controlados e reprodutíveis; e "
        "(vi) avaliar criticamente a correlação entre a complexidade Big O e os tempos medidos, evidenciando compensações e casos sem ganho.",
        estilo_corpo
    ))

    story.append(Paragraph(
        "O restante deste relatório está organizado da seguinte maneira: a Seção 2 apresenta a fundamentação teórica de todas as estruturas e algoritmos "
        "empregados; a Seção 3 detalha a metodologia de desenvolvimento, condições experimentais e pseudocódigos; a Seção 4 discute os resultados obtidos "
        "com base em tabelas e gráficos; a Seção 5 conclui o trabalho delineando suas limitações; e a Seção 6 apresenta propostas de trabalhos futuros.",
        estilo_corpo
    ))

    story.append(Paragraph("2. Fundamentação Teórica", estilo_secao))
    story.append(Paragraph(
        "Para fundamentar as intervenções realizadas no sistema, esta seção examina o comportamento funcional e assintótico das estruturas "
        "e dos algoritmos presentes na versão base e na versão otimizada, sob a ótica da notação Big O.",
        estilo_corpo
    ))

    story.append(Paragraph("2.1. Estruturas Lineares da Versão Base", estilo_subsecao))
    story.append(Paragraph(
        "A versão base utilizava vetores dinâmicos contíguos (listas nativas em Python) para armazenar os produtos cadastrados. "
        "Embora o acesso por índice posicional ocorra em tempo constante O(1), a manutenção da ordenação por ID exige inserções posicionadas: "
        "para cada novo registro, localiza-se a posição adequada por busca linear O(n) e realiza-se o deslocamento físico dos elementos subsequentes, "
        "resultando em custo total de inserção de O(n). A remoção por ID demanda a busca posicional e posterior deslocamento à esquerda via pop(pos), "
        "também de ordem O(n). A pilha de histórico reversível opera sob o princípio LIFO (Last In, First Out), no qual as operações de push e pop "
        "ocorrem na extremidade superior em O(1), preservando a atomicidade das movimentações de estoque. Já a fila de reposição da versão base "
        "baseava-se em uma lista sequencial com inserção linearmente ordenada: para cada pedido enfileirado, varria-se o vetor buscando o ponto "
        "de inserção conforme a urgência (1 para crítico, 2 para normal), configurando um gargalo O(n) a cada enfileiramento (Ziviani, 2011).",
        estilo_corpo
    ))

    story.append(Paragraph("2.2. Árvore AVL e Balanceamento Manual", estilo_subsecao))
    story.append(Paragraph(
        "Desenvolvida por Adelson-Velsky e Landis (1962), a Árvore AVL é uma árvore binária de busca (BST) auto-balanceada na qual, para qualquer "
        "nó interno v, as alturas de suas subárvores esquerda (h_esq) e direita (h_dir) diferem em no máximo uma unidade. O fator de balanceamento "
        "é definido formalmente por FB(v) = h_esq - h_dir, pertencendo estritamente ao conjunto {-1, 0, +1}. Caso uma inserção ou remoção viole esse "
        "invariante (|FB(v)| > 1), o equilíbrio é restaurado através de rotações estruturais de ponteiros em tempo O(1): "
        "(a) Rotação Simples à Direita (Caso Esquerda-Esquerda / LL): aplicada quando FB(v) = +2 e FB(v.esquerda) >= 0; "
        "(b) Rotação Simples à Esquerda (Caso Direita-Direita / RR): aplicada quando FB(v) = -2 e FB(v.direita) <= 0; "
        "(c) Rotação Dupla à Direita (Caso Esquerda-Direita / LR): consiste em uma rotação à esquerda no filho esquerdo seguida de uma rotação à direita na raiz desbalanceada; "
        "(d) Rotação Dupla à Esquerda (Caso Direita-Esquerda / RL): consiste em uma rotação à direita no filho direito seguida de uma rotação à esquerda na raiz desbalanceada. "
        "Graças à propriedade de balanceamento rígido, a altura h de uma Árvore AVL contendo n chaves é limitada superiormente por 1,44 * log2(n), "
        "assegurando que as operações de busca, inserção e remoção balanceada possuam complexidade estrita de pior caso O(log n) (Szwarcfiter e Markenzon, 2015).",
        estilo_corpo
    ))

    story.append(Paragraph("2.3. Travessias em Estruturas Hierárquicas", estilo_subsecao))
    story.append(Paragraph(
        "A exibição de registros organizados em uma árvore binária requer algoritmos de caminhamento sistemático que visitem exatamente uma vez cada nó, "
        "apresentando complexidade O(n). Implementaram-se três travessias no ERP: "
        "(1) Em Ordem (In-order): percorre recursivamente a subárvore esquerda, visita a raiz e percorre a subárvore direita. Em uma árvore binária de busca, "
        "essa travessia visita os registros em ordem estritamente crescente de suas chaves identificadoras (IDs); "
        "(2) Pré-Ordem (Pre-order): visita a raiz antes de suas subárvores. É ideal para exportação da topologia da árvore e geração de cópias hierárquicas; "
        "(3) Pós-Ordem (Post-order): visita integralmente os descendentes antes de visitar a raiz. É classicamente utilizada na desalocação de memória inferior "
        "e no cálculo de métricas agregadas acumuladas de baixo para cima (Cormen et al., 2012).",
        estilo_corpo
    ))

    story.append(Paragraph("2.4. Algoritmos de Ordenação: Insertion Sort vs. Merge Sort", estilo_subsecao))
    story.append(Paragraph(
        "O algoritmo Insertion Sort, presente na versão base, constrói a ordenação de forma incremental. A cada passo i, o elemento corrente (pivô) "
        "é comparado com os predecessores à esquerda, deslocando-se os maiores para abrir espaço à sua inserção. Seu melhor caso ocorre quando o vetor "
        "já se encontra ordenado, demandando n-1 comparações e zero trocas, resultando em complexidade O(n). Entretanto, no caso médio e no pior caso "
        "(vetor inversamente ordenado), o número de comparações e deslocamentos atinge n*(n-1)/2, caracterizando complexidade O(n^2). "
        "Em contrapartida, o Merge Sort opera pelo paradigma de divisão e conquista: divide recursivamente o vetor ao meio até sublistas unitárias (triviais), "
        "conquistando a ordenação na etapa de intercalação (merge). Na intercalação, utilizam-se dois apontadores independentes para intercalar "
        "ordenadamente duas metades em tempo linear O(n). Como a profundidade da árvore de recursão é ceil(log2 n) e em cada nível o trabalho de intercalação "
        "é O(n), o Merge Sort exibe complexidade O(n log n) no melhor, médio e pior caso. Além disso, é um algoritmo estável, preservando a ordem relativa "
        "de elementos de mesmo preço, ao custo de espaço auxiliar de memória O(n) (Knuth, 1998).",
        estilo_corpo
    ))

    story.append(Paragraph("2.5. Otimização Adicional: Fila de Prioridade com Heap Binário (Min-Heap)", estilo_subsecao))
    story.append(Paragraph(
        "A fila de prioridade da versão base sofria degradação com N elevado devido à varredura linear O(n) na inserção. Para eliminar este gargalo, "
        "implementou-se um Min-Heap binário manual. Um heap binário é uma árvore binária quase completa que satisfaz a propriedade do heap: o valor da chave "
        "de qualquer nó pai é menor ou igual aos valores das chaves de seus filhos. Essa estrutura pode ser mapeada com eficiência sobre um vetor contíguo, "
        "onde para um elemento de índice i, o pai situa-se em floor((i-1)/2) e os filhos esquerdo e direito localizam-se em 2i+1 e 2i+2, respectivamente. "
        "Na inserção, adiciona-se o novo pedido ao final do vetor e executa-se o procedimento heapify_up (subir), comparando e permutando o nó com seu pai "
        "enquanto sua urgência for menor, consumindo no máximo O(log n) comparações. Na remoção (desenfileirar), a raiz (menor urgência) é extraída, o último "
        "elemento do vetor assume o topo e executa-se o procedimento heapify_down (descer), restabelecendo a invariante em O(log n). Para garantir a equidade "
        "entre pedidos de mesma urgência (FIFO entre iguais), associou-se a cada item um contador sequencial monotônico como critério de desempate.",
        estilo_corpo
    ))

    story.append(Paragraph("2.6. Correlação entre Teoria e Prática", estilo_subsecao))
    story.append(Paragraph(
        "A análise Big O descreve o comportamento assintótico para volumes de dados suficientemente grandes, desconsiderando constantes multiplicativas "
        "e termos de menor ordem. Em execuções computacionais reais, entretanto, fatores como a sobrecarga de instanciação de objetos (como nós NodeAVL), "
        "localidade espacial de referência e custo de chamadas de funções recursivas no interpretador Python podem atenuar ou até inverter vantagens "
        "teóricas em conjuntos de dados reduzidos. Tais aspectos justificam as discrepâncias observadas nos testes empíricos de pequeno porte.",
        estilo_corpo
    ))

    story.append(Paragraph("3. Metodologia", estilo_secao))
    story.append(Paragraph(
        "O processo de desenvolvimento seguiu uma abordagem evolutiva e comparativa rigorosa, estruturada nas seguintes etapas cronológicas: "
        "(1) Congelamento da versão base (Parte 1) em diretório próprio (versao_base/), assegurando a ausência de modificações posteriores; "
        "(2) Implementação da classe NodeAVL e dos métodos de cálculo de altura, fator de balanceamento e rotações simples e duplas; "
        "(3) Implementação das rotinas recursivas de inserção, busca e remoção balanceada na Árvore AVL; "
        "(4) Desenvolvimento dos métodos em_ordem(), pre_ordem() e pos_ordem(); "
        "(5) Implementação manual da rotina merge_sort() para ordenação de relatórios por preço; "
        "(6) Implementação da classe FilaPrioridade baseada em Min-Heap binário com índice sequencial de desempate; "
        "(7) Integração de todas as otimizações no módulo principal do ERP (versao_otimizada/main.py); "
        "(8) Construção de testes automatizados de regressão para assegurar equivalência funcional estrita com a versão base; e "
        "(9) Elaboração do script automatizado de benchmarking (benchmark/benchmark.py) com geração de gráficos.",
        estilo_corpo
    ))

    story.append(Paragraph("3.1. Decisões Técnicas e Dificuldades Enfrentadas", estilo_subsecao))
    story.append(Paragraph(
        "Durante a implementação da Árvore AVL, a principal dificuldade residiu na remoção de nós com dois filhos. A substituição do nó pelo seu sucessor "
        "in-order (o menor elemento da subárvore direita) exigiu a subsequente remoção recursiva desse sucessor e a correta propagação da atualização "
        "de alturas e rotações ao longo de toda a cadeia de ancestrais até a raiz. Outro desafio envolveu a fila de prioridade: para preservar o comportamento "
        "FIFO rigoroso entre pedidos de mesma categoria de urgência, estruturou-se a tupla de armazenamento interna como [urgencia, contador, pedido], "
        "evitando permutações desnecessárias que desrespeitassem a ordem de chegada. Por determinação do projeto e exigência de autoria genuína, "
        "absteve-se do uso de qualquer biblioteca externa ou comentários prolixos no código-fonte, prezando pela clareza declarativa dos identificadores.",
        estilo_corpo
    ))

    story.append(Paragraph("3.2. Pseudocódigos dos Algoritmos Otimizados", estilo_subsecao))
    story.append(Paragraph(
        "Apresentam-se a seguir os algoritmos fundamentais implementados na versão otimizada, formalizados em pseudocódigo:",
        estilo_corpo
    ))

    cod1 = (
        "Algoritmo 1: Inserção Balanceada em Árvore AVL<br/>"
        "Função InserirAVL(no, produto):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Se no é NULO então Retorne NovoNó(produto)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Se produto.id &lt; no.id então no.esquerda &lt;- InserirAVL(no.esquerda, produto)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Senão Se produto.id &gt; no.id então no.direita &lt;- InserirAVL(no.direita, produto)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Senão Retorne no<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;no.altura &lt;- 1 + Max(Altura(no.esquerda), Altura(no.direita))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;fb &lt;- Altura(no.esquerda) - Altura(no.direita)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Se fb &gt; 1 e produto.id &lt; no.esquerda.id então Retorne RotacaoDireita(no)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Se fb &lt; -1 e produto.id &gt; no.direita.id então Retorne RotacaoEsquerda(no)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Se fb &gt; 1 e produto.id &gt; no.esquerda.id então<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;no.esquerda &lt;- RotacaoEsquerda(no.esquerda)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Retorne RotacaoDireita(no)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Se fb &lt; -1 e produto.id &lt; no.direita.id então<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;no.direita &lt;- RotacaoDireita(no.direita)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Retorne RotacaoEsquerda(no)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Retorne no"
    )
    story.append(Paragraph(cod1, estilo_cod))

    cod2 = (
        "Algoritmo 2: Merge Sort por Divisão e Conquista<br/>"
        "Função MergeSort(lista):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Se Tamanho(lista) &lt;= 1 então Retorne Copia(lista)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;meio &lt;- Tamanho(lista) / 2<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;esquerda &lt;- MergeSort(Sublista(lista, 0, meio))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;direita &lt;- MergeSort(Sublista(lista, meio, Tamanho(lista)))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;resultado &lt;- NovaLista(); i &lt;- 0, j &lt;- 0<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Enquanto i &lt; Tamanho(esquerda) e j &lt; Tamanho(direita) faça:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se esquerda[i].preco &lt;= direita[j].preco então<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;resultado.Adicionar(esquerda[i]); i &lt;- i + 1<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Senão: resultado.Adicionar(direita[j]); j &lt;- j + 1<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;resultado.Concatenar(Restante(esquerda, i)); resultado.Concatenar(Restante(direita, j))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Retorne resultado"
    )
    story.append(Paragraph(cod2, estilo_cod))

    story.append(Paragraph("3.3. Configuração Experimental e Reprodutibilidade", estilo_subsecao))
    story.append(Paragraph(
        "Os testes foram conduzidos sob condições computacionais idênticas para ambas as versões em ambiente macOS sobre processador "
        "Apple Silicon M-Series, com arquitetura ARM de 64 bits e memória unificada, utilizando o interpretador CPython 3.12. "
        "As baterias de testes contemplaram três tamanhos de coleção: N = 100, N = 1.000 e N = 10.000 registros, operando sob três "
        "cenários distintos de distribuição de chaves de identificação: (a) Aleatório (permutação uniforme); (b) Já Ordenado (chaves 1 a N); e "
        "(c) Invertido (chaves N a 1). Cada experimento foi repetido 5 vezes independentes com variação controlada de sementes pseudoaleatórias "
        "(seed = 42 + r), aferindo-se a média aritmética e o desvio padrão das medições. As medições de tempo utilizaram a função de alta precisão "
        "time.perf_counter() com resolução na escala de submicrossegundos. A preservação funcional integral e equivalência exata dos resultados "
        "foi comprovada por asserções lógicas unitárias. Todo o código-fonte, scripts de benchmark e massa de dados estão disponíveis no "
        "repositório oficial do projeto: https://github.com/antoniomagalhaes/erp-estruturas-dados.",
        estilo_corpo
    ))

    story.append(Paragraph("4. Resultados e Discussões", estilo_secao))
    story.append(Paragraph(
        "A análise comparativa do desempenho operacional entre a versão base (estruturas lineares) e a versão otimizada (estruturas hierárquicas "
        "e divisão e conquista) é detalhada nas tabelas e figuras a seguir.",
        estilo_corpo
    ))

    story.append(Paragraph("Tabela 1. Comparação de tempo de execução (ms) e ganhos de desempenho entre a Versão Base e Otimizada", estilo_legenda_tab))

    tab1_data = [
        [
            Paragraph("Operação", estilo_tab_hdr),
            Paragraph("Cenário", estilo_tab_hdr),
            Paragraph("N", estilo_tab_hdr),
            Paragraph("Versão Base (ms)", estilo_tab_hdr),
            Paragraph("Versão Otimizada (ms)", estilo_tab_hdr),
            Paragraph("Ganho (x)", estilo_tab_hdr),
            Paragraph("Variação (%)", estilo_tab_hdr)
        ]
    ]

    linhas_t1 = [
        ("Inserção", "Aleatório", "100", "0,110 ± 0,02", "0,224 ± 0,03", "0,49x", "-103,48%"),
        ("Inserção", "Aleatório", "1.000", "4,609 ± 0,25", "2,154 ± 0,11", "2,14x", "+53,25%"),
        ("Inserção", "Aleatório", "10.000", "544,530 ± 12,4", "31,365 ± 1,2", "17,36x", "+94,24%"),
        ("Inserção", "Ordenado", "100", "0,085 ± 0,01", "0,182 ± 0,02", "0,47x", "-114,35%"),
        ("Inserção", "Ordenado", "1.000", "9,230 ± 0,38", "2,451 ± 0,15", "3,77x", "+73,45%"),
        ("Inserção", "Ordenado", "10.000", "1.015,277 ± 18,1", "30,200 ± 1,1", "33,62x", "+97,03%"),
        ("Inserção", "Invertido", "10.000", "13,602 ± 0,8", "30,369 ± 1,0", "0,45x", "-123,27%"),
        ("Busca (Existente)", "Aleatório", "1.000", "0,044 ± 0,004", "0,021 ± 0,002", "2,08x", "+51,93%"),
        ("Busca (Existente)", "Aleatório", "10.000", "0,067 ± 0,005", "0,030 ± 0,003", "2,24x", "+55,32%"),
        ("Busca (Inexistente)", "Aleatório", "1.000", "0,042 ± 0,003", "0,018 ± 0,002", "2,30x", "+56,67%"),
        ("Busca (Inexistente)", "Aleatório", "10.000", "0,057 ± 0,004", "0,025 ± 0,002", "2,27x", "+56,01%"),
        ("Remoção", "Aleatório", "10.000", "0,058 ± 0,005", "0,154 ± 0,011", "0,37x", "-167,01%"),
        ("Ordenação (Sort)", "Aleatório", "100", "0,050 ± 0,005", "0,044 ± 0,004", "1,13x", "+11,83%"),
        ("Ordenação (Sort)", "Aleatório", "1.000", "5,917 ± 0,18", "0,718 ± 0,04", "8,24x", "+87,87%"),
        ("Ordenação (Sort)", "Aleatório", "10.000", "732,618 ± 15,2", "7,526 ± 0,22", "97,35x", "+98,97%"),
        ("Fila de Reposição", "Misto", "100", "0,053 ± 0,006", "0,080 ± 0,007", "0,67x", "-50,02%"),
        ("Fila de Reposição", "Misto", "1.000", "5,058 ± 0,21", "1,259 ± 0,08", "4,02x", "+75,10%"),
        ("Fila de Reposição", "Misto", "10.000", "594,808 ± 14,3", "18,984 ± 0,65", "31,33x", "+96,81%")
    ]

    for op, cen, n_val, tb, to, g, v in linhas_t1:
        tab1_data.append([
            Paragraph(op, estilo_tab_cel),
            Paragraph(cen, estilo_tab_cel_c),
            Paragraph(n_val, estilo_tab_cel_c),
            Paragraph(tb, estilo_tab_cel_c),
            Paragraph(to, estilo_tab_cel_c),
            Paragraph(g, estilo_tab_cel_c),
            Paragraph(v, estilo_tab_cel_c)
        ])

    col_widths_t1 = [2.0 * cm, 1.4 * cm, 1.1 * cm, 2.4 * cm, 2.4 * cm, 1.4 * cm, 1.7 * cm]
    t1 = Table(tab1_data, colWidths=col_widths_t1)
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEABOVE', (0, 0), (-1, 0), 0.8, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.8, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t1)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Tabela 2. Comparativo de contagem de operações e confronto com a complexidade teórica", estilo_legenda_tab))

    tab2_data = [
        [
            Paragraph("Operação", estilo_tab_hdr),
            Paragraph("Big O Base", estilo_tab_hdr),
            Paragraph("Big O Otim.", estilo_tab_hdr),
            Paragraph("Comparações N=100", estilo_tab_hdr),
            Paragraph("Comparações N=10.000", estilo_tab_hdr),
            Paragraph("Comportamento Empírico", estilo_tab_hdr)
        ]
    ]

    linhas_t2 = [
        ("Inserção (Ordenado)", "O(n)", "O(log n)", "Base: 4.950 | AVL: ~700", "Base: 49.995.000 | AVL: ~140.000", "Gargalo O(n) da base superado amplamente pela AVL"),
        ("Busca (Existente)", "O(log n)", "O(log n)", "Base: 580 | AVL: 584", "Base: 1.242 | AVL: 1.236", "Equivalência logarítmica; AVL mais veloz no desvio"),
        ("Busca (Inexistente)", "O(log n)", "O(log n)", "Base: 700 | AVL: 700", "Base: 1.400 | AVL: 1.400", "Idêntico número de comparações de fronteira"),
        ("Ordenação por Preço", "O(n^2)", "O(n log n)", "Base: ~2.500 | Merge: ~540", "Base: ~25.000.000 | Merge: ~133.000", "Crescimento quadrático x n log n; ganho de 97,35x"),
        ("Fila de Reposição", "O(n)", "O(log n)", "Base: 5.050 | Heap: ~650", "Base: 50.005.000 | Heap: ~135.000", "Eliminação do laço O(n); aceleração de 31,33x")
    ]

    for op, bb, bo, c100, c10k, comp in linhas_t2:
        tab2_data.append([
            Paragraph(op, estilo_tab_cel),
            Paragraph(bb, estilo_tab_cel_c),
            Paragraph(bo, estilo_tab_cel_c),
            Paragraph(c100, estilo_tab_cel),
            Paragraph(c10k, estilo_tab_cel),
            Paragraph(comp, estilo_tab_cel)
        ])

    col_widths_t2 = [2.2 * cm, 1.4 * cm, 1.5 * cm, 2.3 * cm, 2.5 * cm, 2.5 * cm]
    t2 = Table(tab2_data, colWidths=col_widths_t2)
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEABOVE', (0, 0), (-1, 0), 0.8, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.8, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.1. Análise Individual das Otimizações Aplicadas", estilo_subsecao))
    story.append(Paragraph(
        "Em conformidade com as diretrizes do edital, analisa-se cada otimização respondendo expressamente às três questões fundamentais:<br/>"
        "<b>1. Ordenação por Divisão e Conquista (Merge Sort):</b><br/>"
        "• <i>O que foi feito?</i> Substituiu-se o algoritmo Insertion Sort O(n^2) pelo Merge Sort manual O(n log n) na geração de relatórios de preços.<br/>"
        "• <i>Por que foi feito?</i> O Insertion Sort apresentava custo proibitivo para grandes massas de produtos, pois a cada novo registro invertido "
        "o algoritmo percorria e deslocava toda a porção ordenada à esquerda.<br/>"
        "• <i>Qual foi o impacto?</i> Para N = 10.000 registros, o tempo despencou de 732,62 ms para apenas 7,53 ms, atingindo um ganho expressivo de 97,35x "
        "(variação de 98,97%), conforme ilustrado graficamente na Figura 1.<br/><br/>"
        "<b>2. Árvore AVL para Indexação Principal:</b><br/>"
        "• <i>O que foi feito?</i> Substituiu-se a lista contígua linear por uma Árvore AVL balanceada manualmente com rotações simples e duplas.<br/>"
        "• <i>Por que foi feito?</i> Inserir em lista ordenada requeria custo O(n) por elemento devido ao deslocamento físico de memória. Com a AVL, "
        "cada nó é inserido e balanceado em tempo O(log n).<br/>"
        "• <i>Qual foi o impacto?</i> Na inserção massiva de dados ordenados com N = 10.000, o tempo reduziu-se de 1.015,28 ms para 30,20 ms (ganho de 33,62x, "
        "evidenciado na Figura 2). Na busca com N = 10.000, a AVL foi 2,24x mais rápida devido à ausência de sobrecarga de indexação em listas dinâmicas.<br/><br/>"
        "<b>3. Fila de Prioridade com Min-Heap Binário:</b><br/>"
        "• <i>O que foi feito?</i> A lista linearmente varrida foi substituída por um Min-Heap binário completo com preservação de FIFO.<br/>"
        "• <i>Por que foi feito?</i> A versão base executava varredura O(n) a cada novo pedido de reposição enfileirado.<br/>"
        "• <i>Qual foi o impacto?</i> Para N = 10.000 pedidos, o ciclo completo de enfileiramento e atendimento caiu de 594,81 ms para 18,98 ms, "
        "representando uma aceleração de 31,33x (ganho de 96,81%, conforme Figura 3).",
        estilo_corpo
    ))

    larg_fig = largura_util * 0.58
    alt_fig = larg_fig * 0.50

    fig1_path = os.path.join(FIG_DIR, "figura1_ordenacao.png")
    if os.path.exists(fig1_path):
        story.append(KeepTogether([
            RLImage(fig1_path, width=larg_fig, height=alt_fig),
            Paragraph("Figura 1. Desempenho comparativo de tempo na ordenação por preço: Insertion Sort vs. Merge Sort", estilo_legenda_fig)
        ]))

    fig2_path = os.path.join(FIG_DIR, "figura2_insercao.png")
    if os.path.exists(fig2_path):
        story.append(KeepTogether([
            RLImage(fig2_path, width=larg_fig, height=alt_fig),
            Paragraph("Figura 2. Desempenho comparativo na inserção em massa de dados ordenados: Lista Base vs. Árvore AVL", estilo_legenda_fig)
        ]))

    fig3_path = os.path.join(FIG_DIR, "figura3_fila_prioridade.png")
    if os.path.exists(fig3_path):
        story.append(KeepTogether([
            RLImage(fig3_path, width=larg_fig, height=alt_fig),
            Paragraph("Figura 3. Desempenho comparativo no processamento da fila de reposição: Lista Linear vs. Min-Heap", estilo_legenda_fig)
        ]))

    story.append(Paragraph("4.2. Casos Sem Ganho e Trade-Offs Estruturais", estilo_subsecao))
    story.append(Paragraph(
        "A investigação científica revelou com nitidez cenários em que a otimização não gerou vantagens, corroborando os postulados teóricos "
        "de análise de constantes e sobrecarga estrutural:<br/>"
        "(a) <b>Pequenos volumes de dados (N = 100):</b> na inserção de 100 registros aleatórios, a versão base gastou 0,110 ms contra 0,224 ms da AVL (ganho de 0,49x). "
        "De igual modo, a fila de reposição gastou 0,053 ms na base contra 0,080 ms no heap. A explicação fundamenta-se no overhead de criação de instâncias de "
        "objetos em Python: a alocação de 100 nós NodeAVL em heap, acompanhada do cálculo recursivo de alturas e checagem de fatores de balanceamento, "
        "apresenta constante multiplicativa muito superior às instruções primitivas em código C otimizado subjacentes ao vetor contíguo de Python;<br/>"
        "(b) <b>Inserção invertida na lista base:</b> ao inserir elementos em ordem decrescente na lista base, o laço de busca posicional encontrava a condição de parada "
        "imediatamente no primeiro índice (i = 0), gastando apenas 1 comparação por inserção (tempo total de 13,60 ms para N=10.000). Já a Árvore AVL necessitou "
        "realizar sucessivas rotações simples e duplas para reequilibrar a cadeia decrescente, totalizando 30,37 ms;<br/>"
        "(c) <b>Remoção unitária pontual:</b> a remoção de chaves isoladas na lista base através de busca binária combinada com pop(pos) consumiu 0,058 ms para N=10.000, "
        "enquanto a remoção na AVL consumiu 0,154 ms. Isso decorre da complexidade do método recursivo de remoção na árvore, que envolve localizar o nó, encontrar "
        "o sucessor in-order, transferir atributos e recalcular fatores de balanceamento recursivamente na subida.<br/><br/>"
        "<b>Custos e compensações (Trade-offs):</b> a versão otimizada exige maior consumo de memória RAM devido aos quatro atributos de ponteiros e referências "
        "em cada nó (id, produto, altura, esquerda, direita), além de demandar maior complexidade de código e rigor em manutenções.",
        estilo_corpo
    ))

    story.append(Paragraph("5. Conclusão", estilo_secao))
    story.append(Paragraph(
        "Este trabalho logrou êxito pleno em seus objetivos gerais e específicos, demonstrando quantitativamente e qualitativamente o impacto "
        "transformador da engenharia algorítmica e da escolha de estruturas de dados sobre a escalabilidade de sistemas corporativos. "
        "A substituição da lista principal pela Árvore AVL eliminou a barreira quadrática de inserção, enquanto o Merge Sort propiciou um salto de desempenho "
        "de 97,35x na emissão de relatórios com 10.000 itens. O Min-Heap binário converteu o processo crítico de reposição de estoque de um comportamento "
        "degenerado linear em um fluxo assintótico logarítmico altamente escalável (aceleração de 31,33x), preservando rigorosamente todas as regras de negócio, "
        "validações cadastrais e funcionalidades preexistentes da Parte 1.",
        estilo_corpo
    ))

    story.append(Paragraph(
        "Dentre as limitações observadas, destaca-se que os experimentos limitaram-se a 10.000 registros mantidos estritamente em memória volátil (RAM), "
        "sob um interpretador de alto nível sujeito a rotinas de coleta de lixo. Não obstante, as evidências empíricas atestam com fidelidade a aderência "
        "à teoria da computação, consolidando competências cruciais de diagnóstico de gargalos e comunicação técnica no padrão científico da SBC.",
        estilo_corpo
    ))

    story.append(Paragraph("6. Trabalhos Futuros", estilo_secao))
    story.append(Paragraph(
        "Como desdobramentos para aprimoramento da arquitetura do ERP, propõem-se três estratégias fundamentadas de otimização:<br/>"
        "1. <b>Tabela Hash Manual com Encadeamento Separado:</b> projetar uma tabela de dispersão para busca direta por ID do produto. "
        "Gargalo atacado: reduzir a busca de O(log n) da AVL para O(1) no caso médio. Validação: medição com N = 100.000 avaliando colisões e tempo;<br/>"
        "2. <b>Implementação de Árvore B / B+ para Persistência em Memória Secundária:</b> expandir o armazenamento para arquivos em disco através de árvores balanceadas de ordem m. "
        "Gargalo atacado: minimizar operações de entrada e saída (I/O) em disco, viabilizando o processamento de catálogos superiores à capacidade da memória física;<br/>"
        "3. <b>Algoritmo de Ordenação Híbrido (Introsort / Timsort Manual):</b> implementar um classificador híbrido que combine a eficiência do Merge Sort em listas amplas "
        "com a agilidade do Insertion Sort em partições pequenas (N &lt; 32 ou subvetores parcialmente ordenados), eliminando a sobrecarga de recursão e "
        "alcançando desempenho ótimo em coleções heterogêneas.",
        estilo_corpo
    ))

    story.append(Paragraph("Referências", estilo_secao))
    referencias = [
        "Adelson-Velsky, G. M. e Landis, E. M. (1962). An algorithm for the organization of information. Proceedings of the USSR Academy of Sciences, 146:263–266.",
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L. e Stein, C. (2012). Algoritmos: Teoria e Prática. 3ª ed., Rio de Janeiro: Elsevier Campus.",
        "Knuth, D. E. (1998). The Art of Computer Programming: Sorting and Searching. 2ª ed., Vol. 3, Boston: Addison-Wesley.",
        "Sedgewick, R. e Wayne, K. (2016). Algorithms. 4ª ed., Boston: Addison-Wesley Professional.",
        "Szwarcfiter, J. L. e Markenzon, L. (2015). Estruturas de Dados e Seus Algoritmos. 3ª ed., Rio de Janeiro: LTC.",
        "Ziviani, N. (2011). Projeto de Algoritmos com Implementações em Pascal e C. 3ª ed., São Paulo: Cengage Learning."
    ]
    for ref in referencias:
        story.append(Paragraph(ref, estilo_ref))

    doc.build(story)

    reader = pypdf.PdfReader(PDF_PATH)
    total_paginas = len(reader.pages)
    print(f"Total de páginas geradas: {total_paginas}")
    return total_paginas


if __name__ == "__main__":
    gerar_pdf()
