#!/bin/bash
# Run full benchmark suite

set -e

echo "📊 Constitutional Security - Benchmark Suite"
echo "==========================================="

MODEL="llama-3.1-70b-4bit"
OUTPUT_DIR="benchmarks/results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUTPUT_DIR"

echo "🏃 Running full adversarial benchmark (10,000 prompts)..."
python -m benchmarks.run \
    --suite full \
    --model "$MODEL" \
    --output "$OUTPUT_DIR/full_benchmark_${TIMESTAMP}.csv" \
    --adversarial-sources "PromptInject,HijackLLM,CustomAgentic,SandboxEscapes" \
    --verbose

echo ""
echo "🔬 Running ablation study..."
python -m benchmarks.run \
    --ablation \
    --model "$MODEL" \
    --output "$OUTPUT_DIR/ablation_${TIMESTAMP}.csv" \
    --verbose

echo ""
echo "📊 Generating comparison tables..."
python -m benchmarks.report \
    --input "$OUTPUT_DIR/full_benchmark_${TIMESTAMP}.csv" \
    --output "$OUTPUT_DIR/report_${TIMESTAMP}.md"

echo ""
echo "✅ Benchmark complete! Results in $OUTPUT_DIR/"
echo "   - full_benchmark_${TIMESTAMP}.csv"
echo "   - ablation_${TIMESTAMP}.csv"
echo "   - report_${TIMESTAMP}.md"