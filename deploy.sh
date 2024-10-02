#!/bin/bash

set -a
source .env
set +a

cd ./llm_benchmark_chart

helm dependency update

cd ..

# Generate a values file from .env
cat <<EOF > llm_benchmark_chart/values_overrides.yaml
secrets:
  POSTGRES_PASSWORD: "$POSTGRES_PASSWORD"
  API_KEY: "$API_KEY"
EOF

helm upgrade --install llm-benchmark ./llm_benchmark_chart \
  --values llm_benchmark_chart/values_overrides.yaml
