#!/bin/bash
curl -L -O https://github.com/brianfrankcooper/YCSB/releases/download/0.12.0/ycsb-0.12.0.tar.gz
echo "0a71f59d999ed437c5800bc68ad99ba352f471f3fec8deb6c76ddf2eec56ac67  ycsb-0.12.0.tar.gz" \
  | sha256sum -c
