#!/bin/bash
# Verify all 12 policies

set -e

echo "🔍 Constitutional Security - Full Verification Suite"
echo "=================================================="

POLICIES=(
    "psl/examples/P1_prompt_injection.psl"
    "psl/examples/P2_exfiltration.psl"
    "psl/examples/P3_tool_safety.psl"
    "psl/examples/P5_dos.psl"
)

DOMAINS=(
    "verification/domains/P1.json"
    "verification/domains/P2.json"
    "verification/domains/P3.json"
    "verification/domains/P5.json"
)

for i in "${!POLICIES[@]}"; do
    POLICY="${POLICIES[$i]}"
    DOMAIN="${DOMAINS[$i]}"
    NAME=$(basename "$POLICY" .psl)
    
    echo ""
    echo "🔍 Verifying $NAME..."
    echo "   Policy: $POLICY"
    echo "   Domain: $DOMAIN"
    
    # Run verification (Node.js implementation)
    node verification/verify.js \
        --policy "$POLICY" \
        --domain "$DOMAIN" \
        --model llama-3.1-70b-4bit \
        --output "verification/logs/${NAME}.log" \
        --format json
    
    # Check result
    RESULT=$(cat "verification/logs/${NAME}.log" | jq -r '.result.verified')
    if [ "$RESULT" = "true" ]; then
        echo "   ✅ VERIFIED"
    else
        echo "   ❌ FAILED"
        exit 1
    fi
done

echo ""
echo "✅ All policies verified successfully!"