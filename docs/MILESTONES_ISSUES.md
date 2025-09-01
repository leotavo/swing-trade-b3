# Roadmap - Milestones and Issues

- Repository: leotavo/swing-trade-b3
- Generated at: 2025-09-01 00:28:37

---

## Summary

- M1 - Configuração Inicial (#1) - 3 issue(s)
- M2 - Coleta e Preparação de Dados (#2) - 4 issue(s)
- M3 - Estratégia Base Swing Trade (#3) - 3 issue(s)
- M4 - Backtesting Inicial (#4) - 3 issue(s)
- M5 - Notificações e Monitoramento (#5) - 3 issue(s)
- M6 - Ajuste de Parâmetros e Otimização (#6) - 3 issue(s)
- M7 - Modelo de ML Básico (#7) - 3 issue(s)
- M8 - Paper Trading (#8) - 3 issue(s)
- M9 - Observabilidade Básica (#9) - 3 issue(s)
- M10 - Segurança e Compliance (#10) - 3 issue(s)
- M11 - Documentação e Guias (#11) - 3 issue(s)
- M12 - Validação Final do MVP (#12) - 3 issue(s)

---

## M1 - Configuração Inicial (#1)

State: open  |  Created: 2025-08-14T04:46:59Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Preparar ambiente de desenvolvimento e controle de versão.

- [x] [#1](https://github.com/leotavo/swing-trade-b3/issues/1) - Criar repositório GitHub com Python + Poetry - labels: setup, infra
  > Repositório criado com ambiente virtual configurado e poetry install executando sem erros.
  > Release: tag `v0.1.0` (commit 8859cd3), ver `docs/releases/issue-1.md`.
- [x] [#2](https://github.com/leotavo/swing-trade-b3/issues/2) - Configurar .gitignore e convenção de branches - labels: setup
  > .gitignore curado (Python/Poetry/IDE/OS) e convenção de branches definida.
  > Documentação: `CONTRIBUTING.md` (branches + Conventional Commits). Commits: 4bd3d3c, b5295cf, 086d54d, 6d685d2.
  > Release: tag `v0.2.0` (commit TO_FILL), ver `docs/releases/v0.2.0.md`.
- [ ] [#3](https://github.com/leotavo/swing-trade-b3/issues/3) - Criar pipeline inicial no GitHub Actions para lint/testes - labels: ci/cd
  > Pipeline executa lint e testes automatizados com sucesso a cada commit.

---

## M2 - Coleta e Preparação de Dados (#2)

State: open  |  Created: 2025-08-14T04:49:20Z  |  Due: N/A  |  Issues: 4

Milestone description:
> Obter e preparar dados históricos da B3 para análise.

- [ ] [#4](https://github.com/leotavo/swing-trade-b3/issues/4) - Implementar conector API B3 (histórico) - labels: data
  > Consegue baixar pelo menos 1 ano de dados diários sem erros.
- [ ] [#5](https://github.com/leotavo/swing-trade-b3/issues/5) - Rotina de limpeza e normalização dos dados - labels: data
  > Dataset final sem valores nulos, datas ordenadas e colunas padronizadas.
- [ ] [#6](https://github.com/leotavo/swing-trade-b3/issues/6) - Script de atualização diária automática - labels: data, automation
  > Script atualiza dados em menos de 5 minutos e sem duplicatas.
- [ ] [#7](https://github.com/leotavo/swing-trade-b3/issues/7) - Testar resiliência da coleta de dados da B3 (Mitigação de Risco) - labels: risk, qa
  > Sistema lida com falhas de rede ou indisponibilidade da API sem encerrar a execução.

---

## M3 - Estratégia Base Swing Trade (#3)

State: open  |  Created: 2025-08-14T04:51:01Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Implementar lógica inicial de sinais.

- [ ] [#8](https://github.com/leotavo/swing-trade-b3/issues/8) - Implementar estratégia RSI + MACD - labels: strategy
  > Código gera sinais consistentes conforme parâmetros de referência.
- [ ] [#9](https://github.com/leotavo/swing-trade-b3/issues/9) - Configurar parâmetros iniciais de entrada/saída - labels: strategy
  > Parâmetros documentados e carregados automaticamente no sistema.
- [ ] [#10](https://github.com/leotavo/swing-trade-b3/issues/10) - Criar função para gerar sinais baseados nos indicadores - labels: strategy
  > Função retorna sinais coerentes com dados de entrada e parâmetros definidos.

---

## M4 - Backtesting Inicial (#4)

State: open  |  Created: 2025-08-14T04:53:31Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Avaliar desempenho histórico da estratégia.

- [ ] [#11](https://github.com/leotavo/swing-trade-b3/issues/11) - Criar módulo de backtesting - labels: backtesting
  > Criar módulo de backtesting
- [ ] [#12](https://github.com/leotavo/swing-trade-b3/issues/12) - Gerar relatório de métricas básicas (lucro, drawdown, acerto) - labels: report
  > Relatório apresenta métricas calculadas corretamente e salvas em arquivo.
- [ ] [#13](https://github.com/leotavo/swing-trade-b3/issues/13) - Comparar resultados com benchmark (IBOV) - labels: analysis
  > Comparação com benchmark disponível em relatório, com gráfico e estatísticas.

---

## M5 - Notificações e Monitoramento (#5)

State: open  |  Created: 2025-08-14T04:57:11Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Criar sistema básico de alertas.

- [ ] [#14](https://github.com/leotavo/swing-trade-b3/issues/14) - Integração com Telegram para alertas - labels: alerts
  > Bot envia mensagens ao canal configurado sem falhas em 3 testes consecutivos.
- [ ] [#15](https://github.com/leotavo/swing-trade-b3/issues/15) - Mensagens claras com preço-alvo e stop - labels: alerts
  > Mensagens incluem ativo, preço de entrada, alvo e stop.
- [ ] [#16](https://github.com/leotavo/swing-trade-b3/issues/16) - Log local das notificações enviadas - labels: logging
  > Logs gravados com data/hora e conteúdo da mensagem enviada.

---

## M6 - Ajuste de Parâmetros e Otimização (#6)

State: open  |  Created: 2025-08-14T04:58:56Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Melhorar acurácia da estratégia.

- [ ] [#17](https://github.com/leotavo/swing-trade-b3/issues/17) - Criar script para varrer parâmetros - labels: optimization
  > Script testa ao menos 10 combinações diferentes e retorna ranking.
- [ ] [#18](https://github.com/leotavo/swing-trade-b3/issues/18) - Testar variações de stop loss e take profit - labels: strategy
  > Resultados comparativos documentados em tabela.
- [ ] [#19](https://github.com/leotavo/swing-trade-b3/issues/19) - Relatório comparativo das otimizações - labels: report
  > Relatório indica qual configuração teve melhor desempenho.

---

## M7 - Modelo de ML Básico (#7)

State: open  |  Created: 2025-08-14T05:00:34Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Adicionar filtro por aprendizado de máquina.

- [ ] [#20](https://github.com/leotavo/swing-trade-b3/issues/20) - Selecionar algoritmo (RandomForest ou XGBoost) - labels: ml
  > Algoritmo escolhido documentado com justificativa técnica.
- [ ] [#21](https://github.com/leotavo/swing-trade-b3/issues/21) - Treinar modelo com dados históricos - labels: ml
  > Modelo atinge acurácia mínima definida (>X%) em validação cruzada.
- [ ] [#22](https://github.com/leotavo/swing-trade-b3/issues/22) - Integrar previsões como filtro de sinais - labels: strategy, ml
  > Sistema descarta sinais com probabilidade < limite configurado.

---

## M8 - Paper Trading (#8)

State: open  |  Created: 2025-08-14T05:01:56Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Simular operação em tempo real.

- [ ] [#23](https://github.com/leotavo/swing-trade-b3/issues/23) - Integrar API de corretora em modo paper trading - labels: integration
  > Consegue simular envio de ordens com dados fictícios.
- [ ] [#24](https://github.com/leotavo/swing-trade-b3/issues/24) - Executar trades simulados a partir dos sinais - labels: automation
  > Execução sem falhas por 5 dias de simulação contínua.
- [ ] [#25](https://github.com/leotavo/swing-trade-b3/issues/25) - Registrar histórico das operações simuladas - labels: logging
  > Registro de todas as operações com status final e métricas.

---

## M9 - Observabilidade Básica (#9)

State: open  |  Created: 2025-08-14T05:03:24Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Monitorar execução e erros.

- [ ] [#26](https://github.com/leotavo/swing-trade-b3/issues/26) - Dashboard local com métricas (streamlit) - labels: monitoring
  > Dashboard exibe pelo menos 5 métricas relevantes em tempo real.
- [ ] [#27](https://github.com/leotavo/swing-trade-b3/issues/27) - Log estruturado de eventos - labels: logging
  > Logs padronizados em JSON e gravados com sucesso em arquivo.
- [ ] [#28](https://github.com/leotavo/swing-trade-b3/issues/28) - Alerta de falha no pipeline - labels: alerts
  > Alerta enviado em até 1 min após detecção de falha.

---

## M10 - Segurança e Compliance (#10)

State: open  |  Created: 2025-08-14T05:04:50Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Garantir segurança mínima no uso.

- [ ] [#29](https://github.com/leotavo/swing-trade-b3/issues/29) - Configuração de variáveis de ambiente seguras - labels: security
  > Todas as credenciais carregadas via .env ou GitHub Secrets.
- [ ] [#30](https://github.com/leotavo/swing-trade-b3/issues/30) - Controle de acesso ao bot de alertas - labels: security
  > Apenas usuários autorizados conseguem interagir com o bot.
- [ ] [#31](https://github.com/leotavo/swing-trade-b3/issues/31) - Documentar política de uso seguro - labels: docs
  > Documento publicado no repositório com práticas de segurança.

---

## M11 - Documentação e Guias (#11)

State: open  |  Created: 2025-08-14T05:05:54Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Documentar uso e manutenção do sistema.

- [ ] [#32](https://github.com/leotavo/swing-trade-b3/issues/32) - Criar README com instruções de instalação - labels: docs
  > README atualizado e testado em nova instalação limpa.
- [ ] [#33](https://github.com/leotavo/swing-trade-b3/issues/33) - Guia rápido de uso - labels: docs
  > Guia com exemplos de execução e parâmetros.
- [ ] [#34](https://github.com/leotavo/swing-trade-b3/issues/34) - Tutorial de atualização de dados e parâmetros - labels: docs
  > Passo a passo validado com execução bem-sucedida.

---

## M12 - Validação Final do MVP (#12)

State: open  |  Created: 2025-08-14T05:06:59Z  |  Due: N/A  |  Issues: 3

Milestone description:
> Garantir que o MVP está pronto.

- [ ] [#35](https://github.com/leotavo/swing-trade-b3/issues/35) - Testar execução completa do pipeline - labels: qa
  > Pipeline completo executa do início ao fim sem erros.
- [ ] [#36](https://github.com/leotavo/swing-trade-b3/issues/36) - Validar indicadores e sinais - labels: qa
  > Resultados coerentes em relação aos dados de entrada.
- [ ] [#37](https://github.com/leotavo/swing-trade-b3/issues/37) - Apresentar resultados do MVP - labels: report
  > Apresentação com gráficos, métricas e conclusões finais.

---
