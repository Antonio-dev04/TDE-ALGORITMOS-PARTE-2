import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

BENCH_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BENCH_DIR, "resultados_benchmark.json")
FIG_DIR = os.path.join(BENCH_DIR, "..", "relatorio", "figuras")
os.makedirs(FIG_DIR, exist_ok=True)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    dados = json.load(f)["experimentos"]


def extrair_serie(op_nome, cenario=None):
    pontos_base = {}
    pontos_otim = {}
    for d in dados:
        if d["operacao"] == op_nome:
            if cenario is None or d["cenario"] == cenario:
                pontos_base[d["n"]] = d["tempo_base_ms"]
                pontos_otim[d["n"]] = d["tempo_otim_ms"]
    volumes = sorted(list(pontos_base.keys()))
    vals_base = [pontos_base[v] for v in volumes]
    vals_otim = [pontos_otim[v] for v in volumes]
    return volumes, vals_base, vals_otim


def desenhar_grafico(titulo, subtitulo, volumes, vals_base, vals_otim, rotulo_base, rotulo_otim, arquivo_saida):
    largura = 1200
    altura = 750
    img = Image.new("RGB", (largura, altura), "white")
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
        font_rotulos = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
        font_valores = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
        font_legenda = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except Exception:
        font_titulo = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_rotulos = ImageFont.load_default()
        font_valores = ImageFont.load_default()
        font_legenda = ImageFont.load_default()

    draw.text((largura // 2, 40), titulo, fill="#111111", font=font_titulo, anchor="mm")
    draw.text((largura // 2, 75), subtitulo, fill="#555555", font=font_sub, anchor="mm")

    x0 = 140
    y0 = 620
    x1 = 1100
    y1 = 140

    draw.line([(x0, y0), (x1, y0)], fill="#333333", width=3)
    draw.line([(x0, y0), (x0, y1)], fill="#333333", width=3)

    max_val = max(max(vals_base), max(vals_otim)) * 1.15
    if max_val == 0:
        max_val = 1.0

    passos_y = 5
    for i in range(passos_y + 1):
        v = (max_val / passos_y) * i
        y_pos = y0 - (i / passos_y) * (y0 - y1)
        draw.line([(x0 - 8, y_pos), (x1, y_pos)], fill="#E0E0E0", width=1)
        draw.line([(x0 - 8, y_pos), (x0, y_pos)], fill="#333333", width=2)
        txt = f"{v:.1f}" if max_val < 10 else f"{int(v):d}"
        draw.text((x0 - 15, y_pos), f"{txt} ms", fill="#333333", font=font_valores, anchor="rm")

    n_pontos = len(volumes)
    xs = []
    for idx, vol in enumerate(volumes):
        x_pos = x0 + ((idx + 0.5) / n_pontos) * (x1 - x0)
        xs.append(x_pos)
        draw.line([(x_pos, y0), (x_pos, y0 + 8)], fill="#333333", width=2)
        draw.text((x_pos, y0 + 20), f"N = {vol:,}".replace(",", "."), fill="#111111", font=font_rotulos, anchor="mm")

    pontos_coords_base = []
    pontos_coords_otim = []
    for idx in range(n_pontos):
        yb = y0 - (vals_base[idx] / max_val) * (y0 - y1)
        yo = y0 - (vals_otim[idx] / max_val) * (y0 - y1)
        pontos_coords_base.append((xs[idx], yb))
        pontos_coords_otim.append((xs[idx], yo))

    cor_base = "#D9534F"
    cor_otim = "#0275D8"

    for idx in range(n_pontos - 1):
        draw.line([pontos_coords_base[idx], pontos_coords_base[idx + 1]], fill=cor_base, width=4)
        draw.line([pontos_coords_otim[idx], pontos_coords_otim[idx + 1]], fill=cor_otim, width=4)

    r = 7
    for idx in range(n_pontos):
        xb, yb = pontos_coords_base[idx]
        draw.ellipse([(xb - r, yb - r), (xb + r, yb + r)], fill=cor_base, outline="#900", width=2)
        draw.text((xb, yb - 18), f"{vals_base[idx]:.2f} ms", fill=cor_base, font=font_valores, anchor="mm")

        xo, yo = pontos_coords_otim[idx]
        draw.ellipse([(xo - r, yo - r), (xo + r, yo + r)], fill=cor_otim, outline="#004", width=2)
        offset_y = 18 if abs(yo - yb) < 30 else -18
        draw.text((xo, yo + offset_y), f"{vals_otim[idx]:.2f} ms", fill=cor_otim, font=font_valores, anchor="mm")

    leg_x = 750
    leg_y = 120
    draw.rectangle([(leg_x, leg_y), (leg_x + 320, leg_y + 85)], fill="#F9F9F9", outline="#CCCCCC", width=1)
    draw.line([(leg_x + 20, leg_y + 25), (leg_x + 60, leg_y + 25)], fill=cor_base, width=4)
    draw.ellipse([(leg_x + 40 - 5, leg_y + 25 - 5), (leg_x + 40 + 5, leg_y + 25 + 5)], fill=cor_base)
    draw.text((leg_x + 75, leg_y + 25), rotulo_base, fill="#111111", font=font_legenda, anchor="lm")

    draw.line([(leg_x + 20, leg_y + 60), (leg_x + 60, leg_y + 60)], fill=cor_otim, width=4)
    draw.ellipse([(leg_x + 40 - 5, leg_y + 60 - 5), (leg_x + 40 + 5, leg_y + 60 + 5)], fill=cor_otim)
    draw.text((leg_x + 75, leg_y + 60), rotulo_otim, fill="#111111", font=font_legenda, anchor="lm")

    img.save(arquivo_saida, quality=95)
    print(f"Grafico salvo em: {arquivo_saida}")


def main():
    vols, vb, vo = extrair_serie("Ordenação Relatório")
    desenhar_grafico(
        "Desempenho da Ordenação por Preço",
        "Comparação empírica de tempo de execução (ms) para N = 100, 1.000 e 10.000",
        vols, vb, vo,
        "Versão Base (Insertion Sort)",
        "Versão Otimizada (Merge Sort)",
        os.path.join(FIG_DIR, "figura1_ordenacao.png")
    )

    vols, vb, vo = extrair_serie("Inserção", "ordenado")
    desenhar_grafico(
        "Desempenho da Inserção em Massa (Cenário Ordenado)",
        "Comparação empírica de inserção com N = 100, 1.000 e 10.000",
        vols, vb, vo,
        "Versão Base (Lista Linear)",
        "Versão Otimizada (Árvore AVL)",
        os.path.join(FIG_DIR, "figura2_insercao.png")
    )

    vols, vb, vo = extrair_serie("Fila Prioridade (Heap)")
    desenhar_grafico(
        "Desempenho da Fila de Prioridade de Reposição",
        "Comparação empírica de enfileirar e desenfileirar N pedidos de reposição",
        vols, vb, vo,
        "Versão Base (Lista Linear O(n))",
        "Versão Otimizada (Min-Heap O(log n))",
        os.path.join(FIG_DIR, "figura3_fila_prioridade.png")
    )


if __name__ == "__main__":
    main()
