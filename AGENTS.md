# AGENTS.md - Swing Trade B3

> **Instrução:** Sempre que o projeto for atualizado, revise e atualize o README.md para refletir as mudanças.
> **Branches:** Devem começar com `feat/`, `fix/` ou `docs/`; uma automação renomeia branches criadas pelo Codex para esse padrão antes do workflow `branch-name.yml` rodar.
> **Antes do PR:** Verifique se a branch final está conforme.

Gerado automaticamente a partir de **milestones** e **issues** do repositório leotavo/swing-trade-b3.
> Estado: **all** · Limite: **1000** · Gerado em: 2025-08-30 04:09 (America/Bahia)

## Índice

- [AGENTS.md - Swing Trade B3](#agentsmd---swing-trade-b3)
  - [Índice](#índice)
  - [M1 - Configuração Inicial](#m1---configuração-inicial)
  - [M2 - Coleta e Preparação de Dados](#m2---coleta-e-preparação-de-dados)
  - [M3 - Estratégia Base Swing Trade](#m3---estratégia-base-swing-trade)
  - [M4 - Backtesting Inicial](#m4---backtesting-inicial)
  - [M5 - Notificações e Monitoramento](#m5---notificações-e-monitoramento)
  - [M6 - Ajuste de Parâmetros e Otimização](#m6---ajuste-de-parâmetros-e-otimização)
  - [M7 - Modelo de ML Básico](#m7---modelo-de-ml-básico)
  - [M8 - Paper Trading](#m8---paper-trading)
  - [M9 - Observabilidade Básica](#m9---observabilidade-básica)
  - [M10 - Segurança e Compliance](#m10---segurança-e-compliance)
  - [M11 - Documentação e Guias](#m11---documentação-e-guias)
  - [M12 - Validação Final do MVP](#m12---validação-final-do-mvp)

---

## M1 - Configuração Inicial

Preparar ambiente de desenvolvimento e controle de versão.

- [CLOSED] [#1](https://github.com/leotavo/swing-trade-b3/issues/1) Criar repositório GitHub com Python + Poetry
  - **labels:** setup, infra · **updated:** 2025-08-30 05:03

- [OPEN] [#2](https://github.com/leotavo/swing-trade-b3/issues/2) Configurar .gitignore e convenção de branches
  - **labels:** setup · **updated:** 2025-08-14 05:12

- [OPEN] [#3](https://github.com/leotavo/swing-trade-b3/issues/3) Criar pipeline inicial no GitHub Actions para lint/testes
  - **labels:** ci/cd · **updated:** 2025-08-14 05:12

## M2 - Coleta e Preparação de Dados

Obter e preparar dados históricos da B3 para análise.

- [OPEN] [#4](https://github.com/leotavo/swing-trade-b3/issues/4) Implementar conector API B3 (histórico)
  - **labels:** data · **updated:** 2025-08-14 05:12

- [OPEN] [#5](https://github.com/leotavo/swing-trade-b3/issues/5) Rotina de limpeza e normalização dos dados
  - **labels:** data · **updated:** 2025-08-14 05:12

- [OPEN] [#6](https://github.com/leotavo/swing-trade-b3/issues/6) Script de atualização diária automática
  - **labels:** data, automation · **updated:** 2025-08-14 05:12

- [OPEN] [#7](https://github.com/leotavo/swing-trade-b3/issues/7) Testar resiliência da coleta de dados da B3 (Mitigação de Risco)
  - **labels:** risk, qa · **updated:** 2025-08-14 05:13

## M3 - Estratégia Base Swing Trade

Implementar lógica inicial de sinais.

- [OPEN] [#8](https://github.com/leotavo/swing-trade-b3/issues/8) Implementar estratégia RSI + MACD
  - **labels:** strategy · **updated:** 2025-08-14 05:13

- [OPEN] [#9](https://github.com/leotavo/swing-trade-b3/issues/9) Configurar parâmetros iniciais de entrada/saída
  - **labels:** strategy · **updated:** 2025-08-14 05:13

- [OPEN] [#10](https://github.com/leotavo/swing-trade-b3/issues/10) Criar função para gerar sinais baseados nos indicadores
  - **labels:** strategy · **updated:** 2025-08-14 05:13

## M4 - Backtesting Inicial

Avaliar desempenho histórico da estratégia.

- [OPEN] [#11](https://github.com/leotavo/swing-trade-b3/issues/11) Criar módulo de backtesting
  - **labels:** backtesting · **updated:** 2025-08-14 05:13

- [OPEN] [#12](https://github.com/leotavo/swing-trade-b3/issues/12) Gerar relatório de métricas básicas (lucro, drawdown, acerto)
  - **labels:** report · **updated:** 2025-08-14 05:13

- [OPEN] [#13](https://github.com/leotavo/swing-trade-b3/issues/13) Comparar resultados com benchmark (IBOV)
  - **labels:** analysis · **updated:** 2025-08-14 05:14

## M5 - Notificações e Monitoramento

Criar sistema básico de alertas.

- [OPEN] [#14](https://github.com/leotavo/swing-trade-b3/issues/14) Integração com Telegram para alertas
  - **labels:** alerts · **updated:** 2025-08-14 05:14

- [OPEN] [#15](https://github.com/leotavo/swing-trade-b3/issues/15) Mensagens claras com preço-alvo e stop
  - **labels:** alerts · **updated:** 2025-08-14 05:14

- [OPEN] [#16](https://github.com/leotavo/swing-trade-b3/issues/16) Log local das notificações enviadas
  - **labels:** logging · **updated:** 2025-08-14 05:14

## M6 - Ajuste de Parâmetros e Otimização

Melhorar acurácia da estratégia.

- [OPEN] [#17](https://github.com/leotavo/swing-trade-b3/issues/17) Criar script para varrer parâmetros
  - **labels:** optimization · **updated:** 2025-08-14 05:14

- [OPEN] [#18](https://github.com/leotavo/swing-trade-b3/issues/18) Testar variações de stop loss e take profit
  - **labels:** strategy · **updated:** 2025-08-14 05:14

- [OPEN] [#19](https://github.com/leotavo/swing-trade-b3/issues/19) Relatório comparativo das otimizações
  - **labels:** report · **updated:** 2025-08-14 05:14

## M7 - Modelo de ML Básico

Adicionar filtro por aprendizado de máquina.

- [OPEN] [#20](https://github.com/leotavo/swing-trade-b3/issues/20) Selecionar algoritmo (RandomForest ou XGBoost)
  - **labels:** ml · **updated:** 2025-08-14 05:15

- [OPEN] [#21](https://github.com/leotavo/swing-trade-b3/issues/21) Treinar modelo com dados históricos
  - **labels:** ml · **updated:** 2025-08-14 05:15

- [OPEN] [#22](https://github.com/leotavo/swing-trade-b3/issues/22) Integrar previsões como filtro de sinais
  - **labels:** strategy, ml · **updated:** 2025-08-14 05:15

## M8 - Paper Trading

Simular operação em tempo real.

- [OPEN] [#23](https://github.com/leotavo/swing-trade-b3/issues/23) Integrar API de corretora em modo paper trading
  - **labels:** integration · **updated:** 2025-08-14 05:16

- [OPEN] [#24](https://github.com/leotavo/swing-trade-b3/issues/24) Executar trades simulados a partir dos sinais
  - **labels:** automation · **updated:** 2025-08-14 05:16

- [OPEN] [#25](https://github.com/leotavo/swing-trade-b3/issues/25) Registrar histórico das operações simuladas
  - **labels:** logging · **updated:** 2025-08-14 05:16

## M9 - Observabilidade Básica

Monitorar execução e erros.

- [OPEN] [#26](https://github.com/leotavo/swing-trade-b3/issues/26) Dashboard local com métricas (streamlit)
  - **labels:** monitoring · **updated:** 2025-08-14 05:16

- [OPEN] [#27](https://github.com/leotavo/swing-trade-b3/issues/27) Log estruturado de eventos
  - **labels:** logging · **updated:** 2025-08-14 05:17

- [OPEN] [#28](https://github.com/leotavo/swing-trade-b3/issues/28) Alerta de falha no pipeline
  - **labels:** alerts · **updated:** 2025-08-14 05:17

## M10 - Segurança e Compliance

Garantir segurança mínima no uso.

- [OPEN] [#29](https://github.com/leotavo/swing-trade-b3/issues/29) Configuração de variáveis de ambiente seguras
  - **labels:** security · **updated:** 2025-08-14 05:17

- [OPEN] [#30](https://github.com/leotavo/swing-trade-b3/issues/30) Controle de acesso ao bot de alertas
  - **labels:** security · **updated:** 2025-08-14 05:17

- [OPEN] [#31](https://github.com/leotavo/swing-trade-b3/issues/31) Documentar política de uso seguro
  - **labels:** docs · **updated:** 2025-08-14 05:17

## M11 - Documentação e Guias

Documentar uso e manutenção do sistema.

- [OPEN] [#32](https://github.com/leotavo/swing-trade-b3/issues/32) Criar README com instruções de instalação
  - **labels:** docs · **updated:** 2025-08-14 05:17

- [OPEN] [#33](https://github.com/leotavo/swing-trade-b3/issues/33) Guia rápido de uso
  - **labels:** docs · **updated:** 2025-08-14 05:17

- [OPEN] [#34](https://github.com/leotavo/swing-trade-b3/issues/34) Tutorial de atualização de dados e parâmetros
  - **labels:** docs · **updated:** 2025-08-14 05:17

## M12 - Validação Final do MVP

Garantir que o MVP está pronto.

- [OPEN] [#35](https://github.com/leotavo/swing-trade-b3/issues/35) Testar execução completa do pipeline
  - **labels:** qa · **updated:** 2025-08-14 05:18

- [OPEN] [#36](https://github.com/leotavo/swing-trade-b3/issues/36) Validar indicadores e sinais
  - **labels:** qa · **updated:** 2025-08-14 05:18

- [OPEN] [#37](https://github.com/leotavo/swing-trade-b3/issues/37) Apresentar resultados do MVP
  - **labels:** report · **updated:** 2025-08-14 05:18
