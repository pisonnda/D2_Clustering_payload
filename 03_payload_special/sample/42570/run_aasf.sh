#!/usr/bin/bash

cut -d, -f2 42570_0906.csv | grep -f - 42570_special_payloads.lst > 42570_0906_special.lst
