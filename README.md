# Roadmap.sh DevOps Beginner Tutorials (Official)
##  #1 Server Performance Stats
---
**Write a script to analyse basic server performance stats**

Goal of this project is to write a script to analyse server performance stats.

### Requirements
You are required to write a script server-stats.sh that can analyse basic server performance stats. You should be able to run the script on any Linux server and it should give you the following stats:

1. Total CPU usage
2. Total memory usage (Free vs Used including percentage)
3. Total disk usage (Free vs Used including percentage)
4. Top 5 processes by CPU usage
5. Top 5 processes by memory usage

**Stretch goal :** Feel free to optionally add more stats such as os version, uptime, load average, logged in users, failed login attempts etc.

# DevOps 教程
## #1 伺服器效能統計
---
編寫腳本分析基本伺服器效能統計資料
專案目標: 撰寫一個可以分析伺服器效能統計資料的腳本。
### 需求
你需要編寫一個名為 server-stats.sh 的腳本，可以分析基本的伺服器效能統計。  
這個腳本應該能在任何 Linux 伺服器上執行，並提供以下統計資料：

1.總 CPU 使用率
2.總記憶體使用情況（可用與已用，包含百分比）
3.總硬碟使用情況（可用與已用，包含百分比）
4.依 CPU 使用率排序的前 5 個程序
5.依記憶體使用率排序的前 5 個程序

**延伸目標：** 可以選擇性地添加更多統計資料，如作業系統版本、運行時間、平均負載、已登入使用者、登入失敗嘗試等。

0216 Claude 3.5 Sonnet Response
===
我已經為您準備了一個完整的腳本，它不僅實現了基本需求，還包含了延伸目標中提到的額外功能。
```bash
#!/bin/bash

# Text colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}=== Server Performance Statistics ===${NC}"
echo "Generated on: $(date)"
echo "----------------------------------------"

# OS Information
echo -e "${GREEN}OS Information:${NC}"
echo "OS Version: $(cat /etc/os-release | grep PRETTY_NAME | cut -d '"' -f 2)"
echo "Kernel Version: $(uname -r)"
echo "Uptime: $(uptime -p)"
echo "Load Average: $(uptime | awk -F 'load average:' '{print $2}')"
echo "----------------------------------------"

# CPU Usage
echo -e "${GREEN}CPU Usage:${NC}"
echo "Current CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')%"
echo "----------------------------------------"

# Memory Usage
echo -e "${GREEN}Memory Usage:${NC}"
free -h | awk '
/^Mem:/ {
    printf "Total Memory: %s\n", $2
    printf "Used Memory: %s (%.2f%%)\n", $3, $3/$2*100
    printf "Free Memory: %s (%.2f%%)\n", $4, $4/$2*100
    printf "Buffers/Cached: %s\n", $6
}'
echo "----------------------------------------"

# Disk Usage
echo -e "${GREEN}Disk Usage:${NC}"
df -h | awk '$NF=="/"{printf "Total: %s\nUsed: %s (%s)\nFree: %s (%s)\n", $2, $3, $5, $4, 100-$5"%"}'
echo "----------------------------------------"

# Top CPU Processes
echo -e "${GREEN}Top 5 CPU-Consuming Processes:${NC}"
ps aux --sort=-%cpu | head -6 | awk 'NR>1 {printf "%s\t%s%%\t%s\n", $11, $3, $2}'
echo "----------------------------------------"

# Top Memory Processes
echo -e "${GREEN}Top 5 Memory-Consuming Processes:${NC}"
ps aux --sort=-%mem | head -6 | awk 'NR>1 {printf "%s\t%s%%\t%s\n", $11, $4, $2}'
echo "----------------------------------------"

# Additional Statistics
echo -e "${GREEN}Additional Information:${NC}"
echo "Currently Logged In Users:"
who | awk '{print $1}' | sort | uniq
echo ""
echo "Recent Failed Login Attempts:"
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -5 || grep "Failed password" /var/log/secure 2>/dev/null | tail -5
echo "----------------------------------------"
```
讓我為您說明如何使用這個腳本：

首先將腳本儲存為 server-stats.sh
添加執行權限：

```bash
chmod +x server-stats.sh
```
執行腳本：

```bash
./server-stats.sh
```
這個腳本提供了：

作業系統版本和核心版本資訊
系統運行時間
系統負載情況
目前登入的使用者
最近的登入失敗紀錄

腳本使用了顏色輸出來增加可讀性，並對數據進行了格式化處理。請注意，查看某些系統日誌（如登入失敗紀錄）可能需要 root 權限。
