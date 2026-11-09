# Estações e ferrovias

> Status: rascunho consolidado | Confiança: média para bitola e altura de plataforma (secundária aberta); média-baixa para o resto | Última revisão: 2026-11-09

## Resumo
Estação = fluxo entrada -> saguão -> controle -> circulação vertical -> plataforma -> trem, com cobertura e sinalização. Bitola real e plataforma real são documentadas, mas em Minecraft a via tem 1 bloco: a escala é convencional. Receitas aqui são [INT] sem teste.

## Conceito
- [DOC, aberta secundária] Bitola padrão 1.435 mm; Stephenson, Liverpool-Manchester 1830; ~60% das linhas do mundo (Wikipedia "Standard-gauge railway").
- [DOC] Altura de plataforma: UK 915 mm (±25); UE 550 e 760 mm (2002/735/EC); NL 840 mm; HS1 760 mm. A faixa "UK 760-840" da R1 foi REFUTADA (Wikipedia "Railway platform height").
- [DOC] Plataforma ilha vs lateral; faixa tátil ADA 24 pol; faixa de segurança UK 1,5 m a 160-200 km/h (Wikipedia "Railway platform").
- [NV] Offset da borda ao eixo (UK 730 mm), largura mínima de plataforma (2,5 m/4 m): fontes não abertas (Network Rail 404; fórum fraco).
- [DOC, só busca R1] Metrô de Washington: iluminação indireta em bancadas na base da abóbada.

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Plataforma 1 bloco acima da via (915 mm ~ 1 m) | | [INT] da conversão |
| Faixa de segurança de outro material a 1-2 blocos da borda | | [INT] |
| Plataforma lateral 5-8 de largura; ilha 8-12 | sem fonte (largura mínima real: NV) | [INT] |
| Comprimento de estação pequena 20-40 | | [INT] |
| Via: 1 bloco de trilho (`rail`) sobre leito de `gravel`; 3 de largura para legibilidade | não há bitola real em blocos | [INT] |
| Cobertura em tesoura: vão 12-16, altura 7-10, pilares a cada 4-5 | | [INT] |
| Saguão 15x25, pé-direito 8-10, janelão em arco | arco só lê com vão >= ~15 (X03) | [INT] + [TESTADO X03] |
| Subterrânea: abóbada 9-11 de largura, altura 6-8 | abóbada pequena não lê (X01e) | [INT] |
- Tipos: cabeceira (terminal), passante, ilha, lateral [DOC R1]; vitoriana (galpão de ferro e vidro), art déco, moderna.

## Como construir no Bedrock
**Receita: estação passante de 2 plataformas laterais com galpão** [NÃO TESTADO]
1. Via dupla: 2 linhas de `rail` (ou `golden_rail` para trecho de parada) sobre `gravel`, separadas por 6-8 de intervalo; leito de `gravel` 3 de largura por linha.
2. Plataformas laterais de 6 x 30, 1 bloco acima da via, em `smooth_stone` ou `stone_bricks`; faixa de segurança em `polished_andesite` a 1 da borda.
3. Pilares de ferro (`iron_bars` ou `spruce_fence`/`stone_brick_wall` + capitel) a cada 4-5; vigas treliçadas em `iron_bars` e cobertura de vidro (`glass_pane`) ou laje.
4. Cobertura em duas águas 1:2 com `stone_brick_slab` (X01b) ou tesoura de 12-16 de vão, altura 7-10.
5. Edifício de estação (saguão): 15x25, pé-direito 8-10, relógio na fachada, porta 3x5 (P-1..P-4 de `../tecnicas/portas-e-entradas.md`).
6. Passarela/escada entre plataformas: lance reto de 7-8 degraus com cabeça livre (`../tecnicas/escadas-internas.md`).
7. Sinalização: `lantern`, `redstone_torch`, `torch` em postes; placas; bancos virados para a via (E-17: lado das costas).
8. Pára-choque no fim de via terminal; bancos e postes fora do eixo das portas (P-7).
9. Auditoria: porta livre, apoio, caminho com degrau <= 1.

**Receita: estação subterrânea** [NÃO TESTADO]: abóbada de berço de 9-11 de largura em `stone_brick_stairs`/`stone_brick_slab`, colunas a cada 4-6, iluminação indireta nos pés da abóbada, plataforma afastada da parede para a luz [INT]; ver [subterraneas-e-suspensas.md](subterraneas-e-suspensas.md).

## Combina com
[pontes-e-viadutos.md](pontes-e-viadutos.md) · [instalacoes-industriais-e-laboratorios.md](instalacoes-industriais-e-laboratorios.md) · [subterraneas-e-suspensas.md](subterraneas-e-suspensas.md) · [vilas-e-cidades.md](vilas-e-cidades.md) · [../estilos/vitoriano.md](../estilos/vitoriano.md) · [../estilos/industrial-e-brutalista.md](../estilos/industrial-e-brutalista.md) · [../ambientacao/iluminacao-e-atmosfera.md](../ambientacao/iluminacao-e-atmosfera.md)

## Erros comuns
- Plataforma sem altura; trilho que acaba sem pára-choque.
- Cobertura sem apoios; falta de acesso entre plataformas; iluminação uniforme.
- Saguão pequeno; ausência de sinalização.
- Esperar bitola real em Minecraft: o trilho é de 1 bloco.

## Limitações e dúvidas
- Largura e offset reais de plataforma: não verificados.
- Todas as medidas em blocos são [INT] e sem teste; mecânicas de trilho/minecart não foram estudadas.
- Estação vitoriana específica: sem medida lida.

## Fontes e evidências
- Wikipedia "Standard-gauge railway", "Railway platform height", "Railway platform" (abertas, secundárias).
- Network Rail 404; RSSB/GIRT7020 e design-karma, ggwash: só busca.
- X01 e X03 (inclinação e curva).
- Notas: A4_r2.md.
