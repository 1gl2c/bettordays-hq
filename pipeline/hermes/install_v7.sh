#!/bin/bash
# One-time setup for the v7 runner on your Mac. Run:  bash ~/bettordays/engine/install_v7.sh
# 1. Schedules bd_daily_v7.sh for 12:40 PM every day (launchd uses your Mac's clock; keep it on Pacific time).
# 2. Checks that hermes is found.
# Your Mac has to be awake at 12:40. To wake it automatically, run once (asks for your password):
#   sudo pmset repeat wakeorpoweron MTWRFSU 12:35:00
set -e
ENGINE="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$ENGINE/bd_daily_v7.sh"
mkdir -p "$HOME/Library/LaunchAgents"
P="$HOME/Library/LaunchAgents/com.bettordays.v7runner.plist"
sed "s#__ENGINE__#$ENGINE#g" "$ENGINE/com.bettordays.v7runner.plist" > "$P"
launchctl bootout "gui/$(id -u)" "$P" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$P"
echo "Scheduled: bd_daily_v7.sh runs every day at 12:40 PM."
H=$(PATH="$HOME/.local/bin:$HOME/.hermes/bin:/opt/homebrew/bin:/usr/local/bin:$PATH" command -v hermes || true)
if [ -n "$H" ]; then echo "hermes found: $H"; else echo "WARNING: hermes not found. Run 'which hermes' in Terminal and tell Claude the path."; fi
echo "Time zone: $(date +%Z). It should say PST or PDT."
echo "Test it any time with:  bash $ENGINE/bd_daily_v7.sh"
