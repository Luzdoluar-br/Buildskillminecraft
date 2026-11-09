# Castelos e fortalezas

> Status: rascunho consolidado | Confiança: média para terminologia, média-baixa para dimensões (Beaumaris em fonte secundária) | Última revisão: 2026-11-09

## Resumo
Castelo é defesa em profundidade: fosso, portão com torres, muralha com adarve, torres de flanco, pátio e menagem. Beaumaris dá números de referência (muralha ~11 m x 4,7 m). O círculo só lê em torre de diâmetro ~15; torres menores devem ser octógonos.

## Conceito
- [DOC, só busca R1] Castelo concêntrico: dois ou mais anéis, o externo mais baixo para fogo sobreposto; barbacã = obra avançada coberta pelas torres; fosso afasta máquinas de cerco e impede escavação.
- [DOC, aberta secundária] Beaumaris: muralha interna 36 pés (11 m) de altura e 15,5 pés (4,7 m) de espessura; pátio interno 0,75 acre; 6 torres internas; muro externo octogonal; fosso (Wikipedia citando Taylor 2004/Cadw; Cadw direto não aberto). O "16 pés" da R1 foi REFUTADO.
- [NV] Torres no muro externo: Wikipedia diz 12, castlewales.com (amadora) diz 16: divergência NÃO resolvida. Fosso ~5,5 m (castlewales, amadora).
- [INT] A lógica visual é a defesa legível: o olho precisa ver adarve, ameias, portão fortificado e fosso.

## Características / regras
| Elemento | Valor em blocos | Rótulo |
|---|---|---|
| Muralha interna | 11 de altura x 5 de espessura | [INT] por tradução de 11 m x 4,7 m |
| Pátio interno Beaumaris | 0,75 acre ~ 3.000 m²: ~55x55 | [INT] por conta direta (A4_r2) |
| Fosso | 5-6 de largura | [INT] |
| Torre circular | diâmetro >= 15 para ler como círculo; abaixo, octógono ou quadrado chanfrado | [TESTADO X03] |
| Adarve 2 de largura + parapeito 1; ameias alternadas bloco/vazio | | [INT] |
| Portão: 2 torres flanqueando passagem de 3 x 4-5 | | [INT] |
| Cúpula/raio >= 8: lajes dão degrau de meio bloco mais fino (+7% a +24% de blocos) | | [TESTADO X03] |
- Espessura de 4,7 m ~ 5 blocos é muito mais que os "3 de espessura" da R1: a muralha real é uma massa, não uma casca [DOC + INT].
- Planta com recortes e ângulos, não quadrado perfeito; ainda assim Beaumaris é simétrica e concêntrica [DOC secundária].

## Como construir no Bedrock
**Receita: castelo concêntrico pequeno** (NÃO TESTADO como conjunto; técnicas isoladas testadas na Vila e X01/X03)
1. Terreno: patamar elevado; fosso escavado em volta (largura 5-6, profundidade 3-4 [INT]). Água contida por blocos (água cria fluxo).
2. Muralha interna: quadrado/octógono ~55x55 no eixo. Casca de `stone_bricks` com núcleo de `cobblestone`, 5 de espessura, 11 de altura. Encher o núcleo só onde a espessura é visível (topo).
3. Adarve: topo em `stone_brick_slab`; parapeito externo 1 bloco de `stone_bricks` com ameias alternadas; acesso por escada de pedra interna (`stone_brick_stairs`) a cada ~20 blocos.
4. Torres: 6 internas e 2 de portão. Diâmetro 15 se circular; senão octógono 7-9. Altura = muralha + 4 a 6 [INT]. Cobertura cônica não funciona em raio <= 4 (X01e): usar telhado de 4 águas (`tenda`) ou coroa de ameias.
5. Portão: passagem 3x4-5 com verga em `stone_brick_stairs` invertida (padrão P-3 de `../tecnicas/portas-e-entradas.md`), batentes maciços, grade `iron_bars`, ponte em `spruce_planks`.
6. Muro externo mais baixo (~7-8 [INT]) com torres; barbacã estreita diante do portão.
7. Envelhecimento: mistura de `stone_bricks`, `cracked_stone_bricks`, `mossy_stone_bricks` com causa (água no pé da muralha) conforme `../materiais/envelhecimento-e-deterioracao.md`.
8. Interior do pátio: capela, estábulo, poço, menagem 15x15 altura 25-35 [INT]. Pátio vazio = erro.
9. Auditoria: apoio, escadas do adarve com cabeça livre, portão com 2 blocos livres de cada lado.

## Combina com
[../estilos/medieval-europeu-e-fantasia.md](../estilos/medieval-europeu-e-fantasia.md) · [../estilos/gotico.md](../estilos/gotico.md) · [templos-e-monumentos.md](templos-e-monumentos.md) · [pontes-e-viadutos.md](pontes-e-viadutos.md) · [vilas-e-cidades.md](vilas-e-cidades.md) · [../ambientacao/ruinas-e-narrativa.md](../ambientacao/ruinas-e-narrativa.md) · [../ambientacao/terreno-biomas-agua.md](../ambientacao/terreno-biomas-agua.md) · [../materiais/paletas-e-combinacoes.md](../materiais/paletas-e-combinacoes.md)

## Erros comuns
- Muralha fina e lisa sem adarve; torres sem ligação com o adarve.
- Torre redonda pequena que lê como caixa (X03).
- Portão minúsculo; castelo sem fosso nem relevo de terreno; ameias contínuas.
- Quadrado perfeito e simétrico demais fora do estilo concêntrico; pátio vazio.

## Limitações e dúvidas
- Número de torres externas de Beaumaris (12 vs 16): não resolvido.
- Dimensões de Caerphilly: nenhuma medida confiável encontrada.
- Número de torres, altura do muro externo e menagem são [INT] sem fonte.
- Conjunto não testado em render; só partes (X01, X03, Vila).

## Fontes e evidências
- Wikipedia "Beaumaris Castle" (aberta, secundária, cita Taylor 2004/Cadw); castlewales.com (aberta, amadora); Cadw direto: não aberto.
- Wikipedia "Concentric castle" e worldhistory.org: só busca (R1).
- X01 (telhados, abóbada de raio 4 falhou), X03 (círculo >= ~15).
- Notas: A4_tipos_de_estrutura.md, A4_r2.md.
