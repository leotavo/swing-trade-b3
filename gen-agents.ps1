param(
  [string]$Repo   = "leotavo/swing-trade-b3",
  [string]$Out    = ".\AGENTS.md",
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
function ConvertTo-MarkdownSafe([string]$txt, [int]$wrap=160) {
  if (-not $txt) { return "" }
  $t = $txt -replace "`r`n","`n" -replace "`r","`n"
  ($t.Split("`n") | ForEach-Object {
    if ([string]::IsNullOrWhiteSpace($_)) { "" }
    elseif ($_.Length -gt $wrap) { $_.Substring(0,$wrap) + " …" } else { $_ }
  }) -join "`n"
}

function Anchor([string]$h) {
  if (-not $h) { return "" }
  $normalized = $h.Normalize([Text.NormalizationForm]::FormD)
  $sb = New-Object System.Text.StringBuilder
  foreach ($ch in $normalized.ToCharArray()) {
    if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($ch) -ne 'NonSpacingMark') {
      $null = $sb.Append($ch)
    }
  }
  $clean = $sb.ToString().ToLowerInvariant()
  # Keep letters, numbers, spaces and hyphens only
  $clean = $clean -replace "[^a-z0-9\- ]",""
  # Replace spaces with hyphens
  $clean = $clean -replace " +","-"
  # Collapse multiple hyphens and trim
  $clean = $clean -replace "-{2,}","-"
  return $clean.Trim('-')
}

# ====== 1) Milestones: título + descrição + contagens ======
$milestonesJson = gh api "repos/$Repo/milestones?state=all&per_page=100" --jq '[.[] | {number,title,description,open_issues,closed_issues,html_url}]'
$milestones = @()
if ($milestonesJson) { $milestones = $milestonesJson | ConvertFrom-Json }

# Ordem das milestones vinda do GitHub (por número ascendente), com "Sem Milestone" ao final
$MilestoneOrder = @()
if ($milestones -and $milestones.Count -gt 0) {
  $MilestoneOrder = @(
    $milestones | Sort-Object number | Select-Object -ExpandProperty title
  )
}
$MilestoneOrder += "Sem Milestone"

# Índice por título
$msByTitle = @{}
foreach ($m in $milestones) { $msByTitle[$m.title] = $m }

# ====== 2) Issues: título + body + labels + assignees + milestone ======
# Usar gh issue list (com limite) e filtrar PRs automaticamente
$issuesJson = gh issue list --repo $Repo --state $State --limit $Limit --json number,title,state,labels,assignees,updatedAt,url,milestone

$issues = @()
if ($issuesJson) {
  $issues = ($issuesJson | ConvertFrom-Json) | ForEach-Object {
    $labels     = @($_.labels | ForEach-Object { $_.name }) -join ", "
    $assignees  = @($_.assignees | ForEach-Object { $_.login }) -join ", "
    [pscustomobject]@{
      number     = $_.number
      title      = $_.title
      state      = ($_.state).ToUpper()
      url        = $_.url
      body       = $null
      labels     = $labels
      assignees  = $assignees
      milestone  = if ($_.milestone.title) { $_.milestone.title } else { "Sem Milestone" }
      updatedAt  = $_.updatedAt
    }
  }
}

# Ordenar por ordem de milestone definida e por número
$issuesOrdered = $issues | Sort-Object `
  @{Expression={ [array]::IndexOf($MilestoneOrder, $_.milestone) }}, `
  number

# ====== 3) Gerar AGENTS.md ======
$sb = New-Object System.Text.StringBuilder
$null = $sb.AppendLine("# AGENTS.md - Swing Trade B3")
$null = $sb.AppendLine()
$null = $sb.AppendLine("Gerado automaticamente a partir de **milestones** e **issues** do repositório $Repo.")
$null = $sb.AppendLine("> Estado: **$State** · Limite: **$Limit** · Gerado em: $(Get-Date -Format 'yyyy-MM-dd HH:mm') (America/Bahia)")
$null = $sb.AppendLine()
$null = $sb.AppendLine("## Índice")
$null = $sb.AppendLine()
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

  # Âncora HTML explícita para compatibilidade com linters/renderizadores
  $null = $sb.AppendLine(('<a id="{0}"></a>' -f (Anchor $mt)))
  $null = $sb.AppendLine("## $mt")
  $null = $sb.AppendLine()

  # Descrição da milestone (se houver)
  if ($msByTitle.ContainsKey($mt) -and $msByTitle[$mt].description) {
    $msDesc = ConvertTo-MarkdownSafe($msByTitle[$mt].description)
    if ($msDesc) {
      $null = $sb.AppendLine($msDesc)
      $null = $sb.AppendLine()
    }
  }

  foreach ($it in $group) {
    $iBody = ConvertTo-MarkdownSafe($it.body)
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

# Pós-processamento: reduzir múltiplas linhas em branco para uma
$text = $sb.ToString() -replace "(\r?\n){3,}", "`n`n"
# Garantir apenas uma linha em branco no final do arquivo
$text = ($text.TrimEnd()) + "`n"
$text | Set-Content -Path $Out -Encoding utf8
Write-Host "OK: '$Out' gerado (UTF-8), com descrições de milestones e issues, na ordem das milestones."
