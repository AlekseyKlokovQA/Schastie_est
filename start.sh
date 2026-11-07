#!/usr/bin/env bash
# Запуск сайта «Счастье есть»: сайт + админка на трёх портах
# Использование: ./start.sh   (остановить — Ctrl+C)
cd "$(dirname "$0")" || exit 1

PORT_LIST="${PORTS:-8080,3000,8000}"
echo "Запускаю «Счастье есть» на портах: $PORT_LIST"
PORTS="$PORT_LIST" exec python3 app.py
