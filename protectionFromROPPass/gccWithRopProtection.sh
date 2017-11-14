#!/usr/bin/env bash

gcc -m32 -O0 -fno-stack-protector --static -S $1 -o intermediate.S
python ropProtectionPass.py intermediate.S secureCode.S
gcc -m32 -O0 -fno-stack-protector --static secureCode.S
