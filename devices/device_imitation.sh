#!/bin/bash

devices="devices.txt"

> "$devices"

run_script() {
  local script_name=$1
  local start_port=$2
  local end_port=$3
  local device_name=$4

  for ((port=start_port; port<=end_port; port++)); do
    delay=$((RANDOM % 2001 + 500))
    
    python3 "$script_name" "$port" "$delay" &
    
    echo "$device_name:$port:$delay" >> "$devices"
  done
}

run_script "windows.py" 10000 10000 "windows"

run_script "switch.py" 10001 10001 "switch"

echo "Информация о запусках записана в $devices."

