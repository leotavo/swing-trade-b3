param(
  [string]$Repo   = "leotavo/swing-trade-b3",
  [string]$Out    = ".\Agents.md",
  [int]   $Limit  = 1000,   # máx. issues a buscar
  [string]$State  = "all"   # open | closed | all
)

# ====== ENCODING: UTF-8 sem BOM (console + saída) ======
try { chcp 65001 | Out-Null } catch {}
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding  = New-Object System.Text.UTF8Encoding($false)
$PSDefaultParameterValues['Out-File:Encoding']    = 'utf8'
$PSDefaultParameterValues['Set-Content:Encoding'] = 'utf8'

# ====== Helpers ======
function Sanitize-Markdown([string]$txt, [int]$wrap=160) {
  if (-not $txt) { return "" }
  $t = $txt -replace "`r`n","`n" -replace "`r","`n"
  ($t.Split("`n") | ForEach-Object {
    if ([string]::IsNullOrWhiteSpace($_)) { "" }
    elseif ($_.Length -gt $wrap) { $_.Substring(0,$wrap) + " …" } else { $_ }
  }) -join "`n"
}

function Anchor([string]$h) {
  return (($h -replace " ","-" -replace "[^a-zA-Z0-9\-]","").ToLower())
}

# ====== 1) Milestones: título + descrição + contagens ======
$milestonesJson = gh api "repos/$Repo/milestones?state=all&per_page=100" --jq ".[] | {number,title,description,open_issues,closed_issues,html_url}"
$milestones = @()
if ($milestonesJson) { $milestones = $milestonesJson | ConvertFrom-Json }

# Ordem natural das suas milestones
$MilestoneOrder = @(
  "M1 - Configuração Inicial",
  "M2 - Coleta e Preparação de Dados",
  "M3 - Estratégia Base Swing Trade",
  "M4 - Backtesting Inicial",
  "M5 - Notificações e Monitoramento",
  "M6 - Ajuste de Parâmetros e Otimização",
  "M7 - Modelo de ML Básico",
  "M8 - Paper Trading",
  "M9 - Observabilidade Básica",
  "M10 - Segurança e Compliance",
  "M11 - Documentação e Guias",
  "M12 - Validação Final do MVP",
  "Sem Milestone"
)

# Índice por título
$msByTitle = @{}
foreach ($m in $milestones) { $msByTitle[$m.title] = $m }

# ====== 2) Issues: título + body + labels + assignees + milestone ======
# Usar /issues (com paginação) p/ trazer body; filtrar PRs (pull_request existe quando é PR)
$issuesRaw = gh api "repos/$Repo/issues?state=$State&per_page=100" --paginate `
  --jq ".[] | select(has(\"pull_request\")|not) | {number,title,state,html_url,body,labels,assignees,milestone,updated_at}"

$issues = @()
if ($issuesRaw) {
  $issues = ($issuesRaw | ConvertFrom-Json) | ForEach-Object {
    $labels     = @($_.labels | ForEach-Object { $_.name }) -join ", "
    $assignees  = @($_.assignees | ForEach-Object { $_.login }) -join ", "
    [pscustomobject]@{
      number     = $_.number
      title      = $_.title
      state      = ($_.state).ToUpper()
      url        = $_.html_url
      body       = $_.body
      labels     = $labels
      assignees  = $assignees
      milestone  = if ($_.milestone.title) { $_.milestone.title } else { "Sem Milestone" }
      updatedAt  = $_.updated_at
    }
  }
}

# Ordenar por ordem de milestone definida e por número
$issuesOrdered = $issues | Sort-Object `
  @{Expression={ [array]::IndexOf($MilestoneOrder, $_.milestone) }}, `
  number

# ====== 3) Gerar Agents.md ======
$sb = New-Object System.Text.StringBuilder
$null = $sb.AppendLine("# Agents.md — Swing Trade B3")
$null = $sb.AppendLine()
$null = $sb.AppendLine("Gerado automaticamente a partir de **milestones** e **issues** do repositório `$Repo`.")
$null = $sb.AppendLine("> Estado: **$State** · Limite: **$Limit** · Gerado em: $(Get-Date -Format 'yyyy-MM-dd HH:mm') (America/Bahia)")
$null = $sb.AppendLine()
$null = $sb.AppendLine("## Índice")
foreach ($mt in $MilestoneOrder) {
  if ($issuesOrdered | Where-Object { $_.milestone -eq $mt }) {
    $null = $sb.AppendLine("- [$mt](#$(Anchor $mt))")
  }
}
$null = $sb.AppendLine()
$null = $sb.AppendLine("---")
$null = $sb.AppendLine()

foreach ($mt in $MilestoneOrder) {
  $group = $issuesOrdered | Where-Object { $_.milestone -eq $mt }
  if (-not $group) { continue }

  $null = $sb.AppendLine("## $mt")
  $null = $sb.AppendLine()

  # Descrição da milestone (se houver)
  if ($msByTitle.ContainsKey($mt) -and $msByTitle[$mt].description) {
    $msDesc = Sanitize-Markdown($msByTitle[$mt].description)
    if ($msDesc) {
      $null = $sb.AppendLine($msDesc)
      $null = $sb.AppendLine()
    }
  }

  foreach ($it in $group) {
    $iBody = Sanitize-Markdown($it.body)
    $meta  = @()
    if ($it.labels)    { $meta += "**labels:** $($it.labels)" }
    if ($it.assignees) { $meta += "**assignees:** $($it.assignees)" }
    if ($it.updatedAt) { $meta += "**updated:** $(Get-Date $it.updatedAt -Format 'yyyy-MM-dd HH:mm')" }
    $metaStr = ($meta -join " · ")

    $null = $sb.AppendLine("- [$($it.state)] [#$($it.number)]($($it.url)) $($it.title)")
    if ($metaStr) { $null = $sb.AppendLine("  - $metaStr") }
    if ($iBody)   {
      $descIndented = ($iBody.Split("`n") | ForEach-Object { "  > " + $_ }) -join "`n"
      $null = $sb.AppendLine($descIndented)
    }
    $null = $sb.AppendLine()
  }
}

$sb.ToString() | Set-Content -Path $Out -Encoding utf8
Write-Host "OK: '$Out' gerado (UTF-8), com descrições de milestones e issues, ordenado M1→M12."
