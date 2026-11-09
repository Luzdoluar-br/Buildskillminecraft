# Chinês tradicional

> Status: pesquisa só por Wikipédia; proporções e curvatura NÃO verificadas; só a receita de beiral levantado tem base em teste (X01) | Confiança: média-baixa | Última revisão: 2026-11-09

## Resumo
Eixo central, plataforma elevada, pátio, telhado grande e pesado com cantos virados para cima, colunas vermelhas e dougong sob o beiral. Cor e número carregam hierarquia (amarelo imperial, nove baias). Curvatura contínua do beiral e razões cai-fen são lacunas.

## Conceito
- [DOC, aberta (Wikipédia, resumo)] Dougong: dou (blocos) e gong (braços) de madeira encaixados sem cola; transferem carga para as colunas, reduzem esforço nas vigas, ajudam contra sismo; surgiu no Zhou Ocidental, complexo em Tang e Song, depois mais ornamental (Ming: menores e mais numerosos). Templo Foguang: 857.
- [DOC] Yingzao Fashi (Li Jie, **1103**): manual Song com sistema de 8 categorias de madeira, o cai-fen.
- [DOC] Telhados curvam-se para cima nos cantos; hierarquia implícita: hip (imperial, simples ou duplo), multi-inclinado, sweeping, reto (plebeus). Nove jian (baias) só para edifícios imperiais; portões imperiais com cinco arcos, central só do imperador.
- [DOC] Xieshan (par do irimoya): quatro águas com empenas em dois lados, 9 cumeeiras, um ou dois beirais.
- [DOC] Siheyuan: casa principal (zhengfang) ao norte virada ao sul; alas leste e oeste; casa oposta ao sul; edifício de trás (único com dois andares); galerias cobertas; portão no canto sudeste laqueado de vermelho, aldrabas de cobre, tela interna (yingbi), leões de pedra; tijolo cinza e madeira laqueada.
- [DOC] Cores: telha amarela = imperial; azul = céu (Templo do Céu); vermelho em colunas e paredes; verde = bambu/longevidade.
- [DOC] Pagodes: primeiros quadrados, depois frequentemente octogonais; Liaodi 84 m, o mais alto pré-moderno.

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Valores do cai-fen (módulo, fen), razões de vão e altura | a página não detalha | **[NV]** |
| Curvatura de beiral (juzhe, shengqi) | página Chinese_roof_types 404; nada lido | **[NV]** |
| Inclinação de telhado em graus | nenhuma fonte aberta | **[NV]** |
| Número de baias/arcos como hierarquia (9, 5) | só contagens simbólicas | [DOC] |
| Silhueta horizontal, plataforma, eixo simétrico | | [INT] |
| Paleta de colunas (vermelho), base (cinza), telha (cinza/azul-verde; amarela só em palácio) | cores do texto [DOC]; blocos [INT] | [INT] |

## Como construir no Bedrock
**Receita A - salão sobre plataforma, eixo e pátio [NÃO TESTADO como conjunto; técnicas parciais em X01/X02]**
1. Pátio retangular (ex.: 15x11), salão principal ao norte, alas leste/oeste; no palácio simetria estrita, no siheyuan mais livre [INT].
2. Plataforma `stone_bricks` ou `polished_andesite` de 1-2 blocos com escadas à frente.
3. Colunas vermelhas: `red_concrete` ou `stripped_crimson_stem` (`pillar_axis=y`), paredes `white_concrete`/`smooth_stone` recuadas entre colunas (o recuo cria plano, como o shoji em X02 F5).
4. Sob o beiral: 1-3 camadas escalonadas de `*_stairs`/`*_trapdoor` invertidos escuros (dougong aproximado) [NÃO TESTADO].
5. Telhado: escadas `dark_prismarine_stairs`, `deepslate_tile_stairs` ou `oxidized_cut_copper_stairs`; amarelo (`yellow_concrete`) só em palácio [INT].

**Receita B - cantos levantados com dois beirais [TESTADO X01-f, 275 blocos]**
Mesma sequência de `japones-tradicional.md` (Receita B): forro de laje invertida sob o beiral, `tenda` com beiral 2, laje levantada no canto, segundo pavimento menor com segundo beiral. Em X01 "lê como identidade asiática" por menor custo; não distingue chinês de japonês: o diferencial é cor (vermelho/amarelo/azul-verde) e plataforma.

**Receita C - curva do beiral com escada+laje [NÃO TESTADO]**
- Ideia [INT]: nas últimas 3-4 colunas antes do canto, subir 1 bloco por degrau (escada, depois laje levantada), em vez de linha reta; o canto termina com laje/`end_rod`/cerca como "chifre".
- Referência apenas de método: `Molde.telhado_suave_x` alterna escada e laje [TESTADO X01]; aqui seria aplicado só na ponta. Altura exata da curva: [NV] (sem dado de curvatura).

**Receita D - portão** [NÃO TESTADO]: `red_concrete`/`red_nether_brick`, 3 de vão, aldrabas `lantern`/botão, degrau, muro-tela atrás, leões de `stone_brick_stairs`.

**Receita E - pagode** [NÃO TESTADO]: andares em número ímpar [INT, não verificado], octogonal (diâmetro >= 15 para ler curva; abaixo disso assuma octógono declarado [TESTADO X03]), cada andar com beiral e canto levantado, flecha de cobre.

## Combina com
- `japones-tradicional.md`, `../estruturas/templos-e-monumentos.md`, `../estruturas/vilas-e-cidades.md`
- `../fundamentos/composicao-hierarquia-silhueta.md`, `../materiais/paletas-e-combinacoes.md`
- `../tecnicas/telhados-e-beirais.md`, `../tecnicas/portas-e-entradas.md`

## Erros comuns
- Telhado amarelo em casa comum; pagode com andares iguais; sem plataforma; cantos retos.
- Torii japonês num conjunto chinês; portão de qualquer cor.
- Esquecer o pátio (a identidade é o conjunto, não só o salão).
- Afirmar proporção de cai-fen ou grau de curvatura: não verificados.

## Limitações e dúvidas
- Curvatura contínua do beiral: impossível; usar 2-3 degraus.
- Cai-fen e curvatura: [NV]. Fonte sugerida: o texto do Yingzao Fashi em fonte primária/secundária que a pesquisa ainda não abriu.
- Dougong em Minecraft é só alusão visual; nenhum teste.
- O render não valida cor.

## Fontes e evidências
- Wikipédia EN, abertas via resumo: Chinese architecture, Dougong, Siheyuan, East Asian hip-and-gable roof, Yingzao Fashi (rodada 2).
- Chinese_roof_types: 404. Nenhuma fonte primária, UNESCO ou museu aberta.
- `../experimentos/X01-telhados/RESULTADO.md`, `X03-curvas-e-diagonais/RESULTADO.md`.
