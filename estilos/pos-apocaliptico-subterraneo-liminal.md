# Pós-apocalíptico, subterrâneo e liminal

> Status: rascunho; pós-apocalíptico apoiado em X04, os outros dois sem teste | Confiança: média (pós-apocalíptico), baixa (subterrâneo e liminal) | Última revisão: 2026-11-09

## Resumo
Três ambientações, não estilos históricos. Pós-apocalíptico: ruína COM CAUSA mais reaproveitamento humano (TESTADO X04). Subterrâneo: abóbadas, luz indireta, ventilação; fontes fracas. Liminal/dreamcore/Backrooms: estética de internet; receitas de espaço repetitivo [NÃO TESTADO].

## Conceito
- **Pós-apocalíptico** [DOC, literatura]: ruínas, vegetação retomando estradas e cidades, reaproveitamento de materiais (Wikipedia, Post-apocalyptic fiction). Convenção visual de ruínas reais (Detroit): vazio, silêncio, natureza retomando (Guernica, aberta); a ponte para ficção é [INT]. Crítica de "ruin porn" existe [DOC, só busca].
- **Subterrâneo** [DOC só Wikipedia, Earth sheltering]: tipos bermed, in-hill, subterrâneo com átrio; problemas: pouca luz, ar parado, umidade; soluções: átrios, claraboias, ventilação cruzada. Metrô (abóbada, luz indireta na base do arco, plataforma recuada): só blog por busca [NV].
- **Liminal** [DOC, Wikipedia que cita jornalismo]: estética de INTERNET, não estilo acadêmico. Conceito antropológico: van Gennep (1909), Turner. "Liminal space" online: imagens de espaços vazios/transitórios difundidas por 4chan, Reddit e Tumblr por volta de 2019. Backrooms: começou em 12/05/2019 no /x/ do 4chan (ficção de internet); Kane Parsons (2022) fez curta found-footage. Dreamcore: estética dos anos 2020, origem incerta. Ligar a Marc Augé ("não-lugares", 1992) é [INT].

## Características / regras
| Tema | Regra | Status |
|---|---|---|
| Ruína | ordem de falha: cobertura, topos de muro, madeiras/pisos, esquadrias, cantos/empenas | [TESTADO X04], apoiada em guia irlandês de conservação (aberto, seção 3) |
| Causas | tempo/água, impacto, incêndio dão leituras diferentes | [TESTADO X04] |
| Remoção | aleatória deixa ~100 blocos flutuantes e não conta história | [TESTADO X04] |
| Corrosão | ferrugem expansiva fissura o concreto (icorr.org, lido); lascar arestas e expor "vergalhão" | [DOC] + tradução [INT]; bloco de vergalhão [NV] |
| Incêndio | madeira some; pedra/tijolo e chaminé ficam (Ecclesiastical, lido) | [DOC parcial] |
| Subterrâneo | luz pontual quente; poços de luz; ritmo de pilares 4-5 | [INT] |
| Liminal | repetição de módulo, teto baixo, luz uniforme, ausência de gente | [INT] |
Ver método de narrativa em [ruínas e narrativa](../ambientacao/ruinas-e-narrativa.md).

## Como construir no Bedrock
**P1 — ruína por abandono [TESTADO X04-R2, casa 15x11, 2 pisos]**
1. Remover o telhado em manchas, nas águas mais expostas.
2. Topos de parede em dentes (alturas diferentes por coluna); `moss_block`/`grass_block` nos topos que restam.
3. Janelas vazias; arco com 1-2 aduelas faltando; empenas e chaminés isoladas em pé; `cracked_stone_bricks`, `mossy_stone_bricks`.
4. Entulho (blocos caídos) ao pé de cada trecho removido, mais alto junto à parede.
5. Rodar a checagem de blocos flutuantes: o experimento ficou com 1. Vegetação ainda esparsa [limite X04].
**P2 — reaproveitamento improvisado [NÃO TESTADO]**: remendos de `oak_planks`, `iron_trapdoor`, `barrel`, `scaffolding` sobre buracos; lona de `light_gray_wool`; fogueira/`lantern` em um canto; sinal de uso humano (porta tapada, caminho gasto). Sem sinal humano vira só "ruína limpa" [INT].
**P3 — concreto pós-industrial [NÃO TESTADO]**: base brutalista ([industrial-e-brutalista.md](industrial-e-brutalista.md), B1) + `moss_block`, manchas em `cut_copper`/`oxidized_copper` nas arestas; mais dano em varandas e junto à água [INT].

**U1 — galeria subterrânea [NÃO TESTADO]**
1. Corredor 5 de largura x 4 de altura interna, pilares a cada 4-5 blocos [INT].
2. Parede `stone_bricks`/`deepslate_bricks`, piso `polished_deepslate`.
3. Abóbada: raio pequeno não lê (berço de raio 4 falhou, X01 e1/e2). Use teto reto com laje ou raio grande; se curva, aceite o polígono [TESTADO X01/X03].
4. Luz: `lantern` ou `sea_lantern` sob laje na base da abóbada/parede, intervalos de 4; poço de luz com `glass` no teto a cada ~12 [INT]. Ventilação visível: `iron_bars`, `trapdoor`.
5. Níveis de luz e spawn de mobs: [NV], verificar no jogo.

**L1 — corredor liminal [NÃO TESTADO]**
1. Módulo 3 de largura x 3 de altura x 4 de comprimento, repetido 10-20 vezes; piso `light_gray_carpet`/`brown_carpet`; parede `yellow_concrete` ou `smooth_sandstone`; forro liso.
2. Luz: placa de `sea_lantern` ou `glowstone` embutida no forro a cada 4 blocos; 1 ou 2 pontos sem luz.
3. Vãos sem porta, bifurcações sem sentido, salas vazias. Piscinas vazias (poolrooms): `light_blue_concrete`, `quartz_block`.
4. Dreamcore: pastéis, céu aberto, escada que não leva a lugar nenhum [INT]. Sem monstros: o efeito vem da ausência e da escala vazia.
5. Opção: `light_block_15` (existe no Bedrock, invisível) para luz sem bloco visível [NÃO TESTADO].

## Combina com
- [Envelhecimento](../materiais/envelhecimento-e-deterioracao.md), [Ruínas e narrativa](../ambientacao/ruinas-e-narrativa.md), [Iluminação](../ambientacao/iluminacao-e-atmosfera.md), [Subterrâneas](../estruturas/subterraneas-e-suspensas.md).
- [Industrial/brutalista](industrial-e-brutalista.md), [Modernista](modernista-e-contemporaneo.md), [Futurista/cyberpunk](futurista-cyberpunk-solarpunk.md).

## Erros comuns
- Dano aleatório e uniforme; ruína sem causa [TESTADO X04].
- Impacto que deixa o telhado intacto [TESTADO X04, falha conhecida].
- Empena alta intacta sobre parede arrasada (ao contrário do real) [DOC guia irlandês].
- Túnel reto escuro sem hierarquia ou poços de luz [INT].
- Liminal: encher de elementos assustadores ou de variedade [INT].

## Limitações e dúvidas
- Subterrâneo: só Wikipedia e blog; sem fonte institucional. Metrô [NV].
- Liminal: sem medidas documentadas; o módulo 3x3x4 é meu.
- Contexto do projeto VULPUS: nada em `../aulas/` sobre estes temas; sem uso específico declarado.
- X04: impacto não derruba telhado; vegetação não calibrada; comparação com fotos reais não feita.

## Fontes e evidências
- Wikipedia: Post-apocalyptic fiction, Earth sheltering, Liminal space (aesthetic), The Backrooms, Dreamcore (aesthetic), Non-place (rodada 1).
- Abertas: PDF "Ruins: Conservation and Repair of Masonry Ruins" (Irlanda, 2010, seção 3); icorr.org; Ecclesiastical (PDF); Guernica; tese Columbia College. Historic England 403; ggwash 403 (só busca).
- `../experimentos/X04-ruinas-com-causa/RESULTADO.md`, `../experimentos/X01-telhados/RESULTADO.md`, `../experimentos/X03-curvas-e-diagonais/RESULTADO.md`.
