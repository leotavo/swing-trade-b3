# scripts/export-roadmap.ps1  (markdownlint/Prettier friendly)
$ErrorActionPreference = 'Stop'

function Get-Truncated([string]$Text, [int]$Max = 600) {
  if ([string]::IsNullOrWhiteSpace($Text)) { return "" }
  $t = $Text.Trim()
  if ($t.Length -le $Max) { return $t }
  return ($t.Substring(0, $Max).Trim() + " ...")
}
function Add-Line($Path, [string]$Text = "") { $Text | Out-File -FilePath $Path -Append -Encoding utf8 }
function Add-BlockQuote($Path, [string]$Text, [string]$Prefix = "> ") {
  if ([string]::IsNullOrWhiteSpace($Text)) { return }
  foreach ($ln in ($Text -split "(`r`n|`n|`r)")) { Add-Line $Path ($Prefix + $ln) }
}
function Get-SubIssueNumbers([string]$Body) {
  $set = New-Object 'System.Collections.Generic.HashSet[int]'
  if ([string]::IsNullOrWhiteSpace($Body)) { return @() }
  foreach ($m in [regex]::Matches($Body, '^\s*-\s*\[[ xX]\]\s*#(\d+)', [System.Text.RegularExpressions.RegexOptions]::Multiline)) { [void]$set.Add([int]$m.Groups[1].Value) }
  if ($set.Count -eq 0) { foreach ($m in [regex]::Matches($Body, '#(\d+)')) { [void]$set.Add([int]$m.Groups[1].Value) } }
  return ($set | Sort-Object -Unique)
}
function Coalesce($Value, $Fallback) { if ($null -ne $Value -and $Value -ne "") { $Value } else { $Fallback } }
function Add-Blank($Path) {
  $last = if (Test-Path $Path) { Get-Content $Path -Tail 1 } else { "" }
  if ($last -ne "") { Add-Line $Path "" }
}

if (-not (Test-Path .git)) { throw "Execute na raiz do repo (onde existe .git/)." }
try { chcp 65001 > $null } catch {}
try { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new() } catch {}

$repo = gh repo view --json nameWithOwner -q .nameWithOwner

$docsDir = Join-Path (Get-Location) 'docs'
New-Item -ItemType Directory -Force -Path $docsDir | Out-Null
$outPath = Join-Path $docsDir 'MILESTONES_ISSUES.md'
Remove-Item $outPath -Force -ErrorAction SilentlyContinue

# --- coleta ---
$milestones = gh api "repos/$repo/milestones?state=all" --paginate | ConvertFrom-Json
$milestonesOrdered = $milestones | Sort-Object { [datetime]$_.created_at }
$issuesRaw = gh api "repos/$repo/issues?state=all&per_page=100" --paginate | ConvertFrom-Json
$issues = $issuesRaw | Where-Object { -not $_.pull_request }
$issueByNumber = @{}; foreach ($i in $issues) { $issueByNumber[$i.number] = $i }

# --- header ---
Add-Line $outPath "# Roadmap - Milestones and Issues"
Add-Blank $outPath
Add-Line $outPath "> AUTO-GERADO — NÃO EDITAR MANUALMENTE"
Add-Line $outPath "> Gere via scripts/export-roadmap.ps1 ou pelo workflow de CI."
Add-Blank $outPath
Add-Line $outPath ("- Repository: " + $repo)
Add-Line $outPath ("- Generated at: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Add-Line $outPath ("- Updated at:   " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Add-Blank $outPath
Add-Line $outPath "---"
Add-Blank $outPath

# --- summary (sem links internos pra evitar MD033) ---
Add-Line $outPath "## Summary"
Add-Blank $outPath
foreach ($m in $milestonesOrdered) {
  $total = $m.open_issues + $m.closed_issues
  Add-Line $outPath ("- " + $m.title + " (#" + $m.number + ") - " + $total + " issue(s)")
}
$issuesNoMs = $issues | Where-Object { -not $_.milestone }
if ($issuesNoMs.Count -gt 0) { Add-Line $outPath ("- (no milestone) - " + $issuesNoMs.Count + " issue(s)") }
Add-Blank $outPath
Add-Line $outPath "---"
Add-Blank $outPath

# --- milestones ---
foreach ($m in $milestonesOrdered) {
  Add-Line $outPath ("## " + $m.title + " (#" + $m.number + ")")
  Add-Blank $outPath
  Add-Line $outPath ("State: " + $m.state + "  |  Created: " + $m.created_at + "  |  Due: " + (Coalesce $m.due_on "N/A") + "  |  Issues: " + ($m.open_issues + $m.closed_issues))
  Add-Blank $outPath
  if ($m.description) {
    Add-Line $outPath "Milestone description:"
    Add-BlockQuote $outPath (Get-Truncated $m.description 1200)
    Add-Blank $outPath
  }

  $msIssues = $issues | Where-Object { $_.milestone -and $_.milestone.number -eq $m.number } | Sort-Object number
  if ($msIssues.Count -eq 0) {
    Add-Line $outPath "(No issues in this milestone.)"
    Add-Blank $outPath
    Add-Line $outPath "---"
    Add-Blank $outPath
    continue
  }

  # lista de issues (com linha em branco antes e depois)
  foreach ($it in $msIssues) {
    $checkbox = if ($it.state -ieq 'open') { "[ ]" } else { "[x]" }
    $labels   = if ($it.labels) { ($it.labels | Select-Object -ExpandProperty name) -join ", " } else { "" }
    $assigs   = if ($it.assignees) { ($it.assignees | Select-Object -ExpandProperty login) -join ", " } else { "" }
    $labelsTxt = if ($labels) { " - labels: " + $labels } else { "" }
    $asTxt     = if ($assigs) { " - assignees: " + $assigs } else { "" }

    # link da issue sempre markdown (evita MD034)
    $link = "[" + ("#" + $it.number) + "](" + $it.html_url + ")"
    Add-Line $outPath ("- " + $checkbox + " " + $link + " - " + $it.title + $labelsTxt + $asTxt)

    if ($it.body) { Add-BlockQuote $outPath (Get-Truncated $it.body 800) "  > " }

    # subissues (links markdown)
    $subs = Get-SubIssueNumbers $it.body
    $subs = $subs | Where-Object { $_ -ne $it.number -and $issueByNumber.ContainsKey($_) } | Select-Object -Unique
    if ($subs.Count -gt 0) {
      Add-Line $outPath "  - Subissues:"
      foreach ($sid in $subs) {
        $si = $issueByNumber[$sid]
        $scheck  = if ($si.state -ieq 'open') { "[ ]" } else { "[x]" }
        $slabels = if ($si.labels) { ($si.labels | Select-Object -ExpandProperty name) -join ", " } else { "" }
        $slabelsTxt = if ($slabels) { " - labels: " + $slabels } else { "" }
        $slink = "[" + ("#" + $si.number) + "](" + $si.html_url + ")"
        Add-Line $outPath ("    - " + $scheck + " " + $slink + " - " + $si.title + $slabelsTxt)
        if ($si.body) { Add-BlockQuote $outPath (Get-Truncated $si.body 400) "      > " }
      }
    }
  }
  Add-Blank $outPath
  Add-Line $outPath "---"
  Add-Blank $outPath
}

# --- bloco (no milestone) ---
if ($issuesNoMs.Count -gt 0) {
  Add-Line $outPath "## (no milestone)"
  Add-Blank $outPath
  foreach ($it in ($issuesNoMs | Sort-Object number)) {
    $checkbox = if ($it.state -ieq 'open') { "[ ]" } else { "[x]" }
    $labels   = if ($it.labels) { ($it.labels | Select-Object -ExpandProperty name) -join ", " } else { "" }
    $assigs   = if ($it.assignees) { ($it.assignees | Select-Object -ExpandProperty login) -join ", " } else { "" }
    $labelsTxt = if ($labels) { " - labels: " + $labels } else { "" }
    $asTxt     = if ($assigs) { " - assignees: " + $assigs } else { "" }
    $link = "[" + ("#" + $it.number) + "](" + $it.html_url + ")"
    Add-Line $outPath ("- " + $checkbox + " " + $link + " - " + $it.title + $labelsTxt + $asTxt)
    if ($it.body) { Add-BlockQuote $outPath (Get-Truncated $it.body 800) "  > " }
  }
}

Write-Host ("Generated: " + $outPath) -ForegroundColor Green
