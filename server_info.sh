#!/bin/sh

echo "📡 *Сеть:*"
ip -4 a | grep -E 'inet ' | awk '{print "🌍 " $2}'

echo ""
echo "📊 *Топ 5 процессов по памяти:*"
ps aux --sort=-%mem | head -n 6 | awk '{print $2, $11, $4"%"}'

echo ""
echo "📦 *Использование swap:*"
free -h | grep "Swap"
