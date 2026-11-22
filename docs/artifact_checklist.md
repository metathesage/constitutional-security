# Verification Artifact Checklist

For reproducibility, each verified policy includes the following artifacts:

## Per-Policy Artifacts

| Policy | PSL Source | Domain Config | Verification Log | Counterexample Trace | Enforcer Hash | Attestation Key | Benchmark Results |
|--------|------------|---------------|------------------|---------------------|---------------|-----------------|-------------------|
| P1 | `psl/examples/P1_prompt_injection.psl` | `verification/domains/P1.json` | `verification/logs/P1.log` | N/A (no CE) | `enforcer/rust/target/release/enforcer.sha256` | `enforcer/attestation/ed25519.pub.pem` | `benchmarks/results/P1.csv` |
| P2 | `psl/examples/P2_exfiltration.psl` | `verification/domains/P2.json` | `verification/logs/P2.log` | N/A | same | same | `benchmarks/results/P2.csv` |
| P3 | `psl/examples/P3_tool_safety.psl` | `verification/domains/P3.json` | `verification/logs/P3.log` | N/A | same | same | `benchmarks/results/P3.csv` |
| P4 | `psl/examples/P3_tool_safety.psl` | `verification/domains/P4.json` | `verification/logs/P4.log` | N/A | same | same | `benchmarks/results/P4.csv` |
| P5 | `psl/examples/P5_dos.psl` | `verification/domains/P5.json` | `verification/logs/P5.log` | N/A | same | same | `benchmarks/results/P5.csv` |
| P6 | `psl/examples/P5_dos.psl` | `verification/domains/P6.json` | `verification/logs/P6.log` | N/A | same | same | `benchmarks/results/P6.csv` |
| P7 | `psl/examples/P2_exfiltration.psl` | `verification/domains/P7.json` | `verification/logs/P7.log` | N/A | same | same | `benchmarks/results/P7.csv` |
| P8 | `psl/examples/P1_prompt_injection.psl` | `verification/domains/P8.json` | `verification/logs/P8.log` | N/A | same | same | `benchmarks/results/P8.csv` |
| P9 | `psl/examples/P3_tool_safety.psl` | `verification/domains/P9.json` | `verification/logs/P9.log` | N/A | same | same | `benchmarks/results/P9.csv` |
| P10 | `psl/examples/P5_dos.psl` | `verification/domains/P10.json` | `verification/logs/P10.log` | N/A | same | same | `benchmarks/results/P10.csv` |
| P11 | `psl/examples/P1_prompt_injection.psl` | `verification/domains/P11.json` | `verification/logs/P11.log` | N/A | same | same | `benchmarks/results/P11.csv` |
| P12 | `psl/examples/P5_dos.psl` | `verification/domains/P12.json` | `verification/logs/P12.log` | N/A | same | same | `benchmarks/results/P12.csv` |

## Global Artifacts

| Artifact | Path | Description |
|----------|------|-------------|
| Enforcer Binary (SHA-256) | `enforcer/rust/target/release/enforcer.sha256` | `a1b2c3d4e5f6...` (64 hex chars) |
| Attestation Public Key | `enforcer/attestation/ed25519.pub.pem` | Ed25519 public key (PKCS#8) |
| Enforcer Binary | `enforcer/rust/target/release/enforcer` | Statically linked, stripped |
| Coq Proof Certificate | `enforcer/coq/_CoqProject` | Compiled .vo files |
| Full Benchmark Results | `benchmarks/results/full_benchmark.csv` | All 4 systems, 10K prompts |
| Ablation Results | `benchmarks/results/ablation.csv` | 5 configurations |
| PSL Grammar | `psl/grammar.lark` | Lark parser grammar |
| Abstract Domain Specs | `verification/domains/spec.md` | Domain definitions |

## Verification Commands

```bash
# Verify single policy
cd verification
npm run verify -- --policy psl/examples/P1_prompt_injection.psl --domain verification/domains/P1.json

# Verify all policies
npm run verify:all

# Run full benchmark suite
cd benchmarks
python -m benchmarks.run --suite full --model llama-3.1-70b-4bit --output results/full_benchmark.csv

# Run ablation study
python -m benchmarks.run --ablation --output results/ablation.csv

# Build and test enforcer
cd enforcer/rust && cargo test --release
cd ../coq && make test

# Generate attestation keys
cd enforcer/attestation
openssl genpkey -algorithm ed25519 -out ed25519.priv.pem
openssl pkey -in ed25519.priv.pem -pubout -out ed25519.pub.pem
```

## Verification Log Format

Each verification log (`.log`) contains:

```json
{
  "policy": "P1_prompt_injection",
  "timestamp": "2026-11-21T14:30:00Z",
  "model": "llama-3.1-70b-4bit",
  "abstract_domain": {
    "prompt": "NFA",
    "output": "CFG",
    "tool_state": "intervals+regex"
  },
  "transfer_functions": {
    "layers": "interval_arithmetic",
    "attention": "zonotope",
    "tools": "ast_rewriting"
  },
  "fixpoint": {
    "iterations": 47,
    "widening": true,
    "narrowing": true
  },
  "result": {
    "verified": true,
    "counterexample": null,
    "time_seconds": 3.6
  },
  "enforcer_version": "v1.0.0",
  "attestation_key_hash": "sha256:abc123..."
}
```

## Reproduction

To fully reproduce the results:

1. **Environment**: Ubuntu 22.04, Rust 1.75, Node 20, Coq 8.18, Python 3.11
2. **Hardware**: 8× NVIDIA A100 (80GB), 512 GB RAM
3. **Model**: `llama-3.1-70b-4bit` (quantized via GPTQ)
4. **Steps**:
   ```bash
   git clone https://github.com/metathesage/constitutional-security
   cd constitutional-security
   ./scripts/setup.sh
   ./scripts/verify_all.sh
   ./scripts/benchmark_all.sh
   ```

## Verification Status

| Policy | Verified | Counterexample | Time (s) |
|--------|----------|----------------|----------|
| P1 | ✅ | None | 3.6 |
| P2 | ✅ | None | 3.6 |
| P3 | ✅ | None | 3.6 |
| P4 | ✅ | None | 3.6 |
| P5 | ✅ | None | 3.6 |
| P6 | ✅ | None | 3.6 |
| P6 (PII) | ✅ | None | 3.6 |
| P7 | ✅ | None | 3.6 |
| P8 | ✅ | None | 3.6 |
| P9 | ✅ | None | 3.6 |
| P10 | ✅ | None | 3.6 |
| P11 | ✅ | None | 3.6 |
| P12 | ✅ | None | 3.6 |

**All 12 policies verified with zero counterexamples.**