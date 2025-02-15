#!/bin/sh
echo "📡 *Сеть:*"
echo "↔️ Интерфейсы:"
ip -brief address | grep -v "lo"

echo ""
echo "📊 *Процессы:*"
ps -eo pid,comm,%cpu,%mem --sort=-%mem | head -n 6

echo ""
echo "📦 *Использование swap:*"
free -h | grep "Swap"
