@echo off
REM ============================================================
REM  TrueVow Night Shift - one-click CTO Orchestrator v2 cycle
REM  Safe/read-only: scans repos, refreshes board, computes ready
REM  tickets, prints founder report. Never deploys or commits.
REM  Schedule me with Windows Task Scheduler for true overnight runs.
REM ============================================================
cd /d C:\Users\yasha\OneDrive\Documents\TrueVow\Cursor
echo [1/3] Syncing shared memory...
python TrueVow_Shared_Orchestration\orchestrator.py sync-memory
echo.
echo [2/3] Running CTO shift cycle...
python TrueVow_Shared_Orchestration\cto_v2.py shift
echo.
echo [3/3] Done. Board: TrueVow_CTO_Knowledge_Orchestrator\KANBAN-BOARD.md
pause
