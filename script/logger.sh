#!/bin/bash

warn() {
  echo -e "\033[33m[WARN] $1\033[0m"
}

error() {
  echo -e "\033[31m[ERROR] $1\033[0m" >&2
  exit 1
}

success_info() {
  echo -e "\033[32m[INFO] $1\033[0m"
}

info() {
  echo "[INFO] $1"
}
