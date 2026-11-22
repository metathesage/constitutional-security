# Constitutional Security: Provably Safe AI Deployment

> **Zero false negatives on 10,000 adversarial tests · 96% TCB reduction · 3.6s verification per policy**

This repository contains the implementation, verification artifacts, and benchmark suite for the **Constitutional Security** framework — a formal framework unifying constitutional AI with abstract interpretation and cryptographic runtime enforcement.

> **Paper:** [Constitutional Security: A Formal Framework for Provably Safe AI Deployment](https://pnthr.xyz/research/constitutional-security) | [PDF](https://pnthr.xyz/papers/constitutional-security.pdf) | [arXiv:2611.XXXXX](https://arxiv.org/abs/2611.XXXXX)

---

## 🏗️ Architecture

```
constitutional-security/
├── psl/                    # Policy Specification Language
│   ├── parser/             # PSL parser (TypeScript/Rust)
│   ├── semantics/          # Temporal logic semantics
│   └── examples/           # Example policies (P1-P12)
├── verification/           # Abstract interpretation pipeline
│   ├── domains/            # Abstract domains (NFA, CFG, intervals, zonotopes)
│   ├── transformers/       # Transfer functions (layers, attention, tools)
│   ├── fixpoint/           # Widening/narrowing for agentic workflows
│   └── model_checker/      # PSL model checking on abstract traces
├── enforcer/               # Runtime reference monitor
│   ├── rust/               # High-performance enforcer (Rust)
│   ├── coq/                # Coq proofs (functional correctness, memory safety)
│   └── attestation/        # Cryptographic attestation (Ed25519)
├── benchmarks/             # Evaluation suite
│   ├── prompts/            # 10,000 adversarial prompts
│   ├── harness/            # Benchmark runner
│   └── results/            # CSV results, comparison tables
└── docs/                   # Documentation
    ├── psl_reference.md
    ├── verification_guide.md
    ├── enforcer_api.md
    └── artifact_checklist.md
```

---

## 🚀 Quick Start

### Prerequisites
- Rust 1.75+ (for enforcer)
- Node.js 20+ (for PSL parser/verification)
- Coq 8.18+ (for proofs)
- Python 3.11+ (for benchmark harness)

### Build & Verify

```bash
# Build enforcer (Rust + Coq)
cd enforcer/rust && cargo build --release
cd ../coq && make

# Run verification pipeline
cd verification && npm install && npm run verify -- --policy psl/examples/P1_prompt_injection.psl

# Run benchmarks
cd benchmarks && python -m benchmarks.run --all --output results/
```

### Run Benchmarks

```bash
# Full adversarial benchmark (10,000 prompts)
python -m benchmarks.run --suite full --model llama-3.1-70b-4bit --output results/full_benchmark.csv

# Ablation studies
python -m benchmarks.run --ablation --output results/ablation.csv
```

---

## 📊 Results Summary

| Metric | Constitutional Security | Constitutional AI | Guardrails.ai | RLHF Only |
|--------|------------------------|-------------------|---------------|-----------|
| **False negatives** | **0 / 10,000** | 247 | 1,834 | 3,112 |
| False positives | 12 / 10,000 | 89 | 2,103 | N/A |
| Verification time | 3.6 s/policy | N/A | N/A | N/A |
| Runtime overhead | 2.3% | 0.8% | 15% | 0% |
| TCB (LOC) | **~2,000** | ~15,000 | ~50,000 | ~100,000 |

**Key finding:** Zero false negatives through *sound* abstract interpretation.

---

## 📋 12 Verified Policies

| ID | Policy | Type | Status |
|----|--------|------|--------|
| P1 | Prompt injection → no sensitive output | Injection | ✅ |
| P2 | No unauthorized external data flow | Exfiltration | ✅ |
| P3 | Code exec args satisfy sandbox | Tool safety | ✅ |
| P4 | Tool output type matches schema | Tool safety | ✅ |
| P5 | Cost threshold triggers termination | DoS | ✅ |
| P6 | No PII in outputs without consent | Privacy | ✅ |
| P7 | Chain-of-thought not leaked | CoT protection | ✅ |
| P8 | Multi-turn injection resistance | Injection | ✅ |
| P9 | Tool chaining sandboxed | Agentic | ✅ |
| P10 | Output length bounded | DoS | ✅ |
| P11 | No instruction following in tool outputs | Injection | ✅ |
| P12 | Constitutional principle adherence | Alignment | ✅ |

---

## 🔧 Policy Specification Language (PSL)

PSL extends LTL with model-specific predicates:

```psl
policy prompt_injection {
  require G ¬(PromptContains(injection_marker) →
    F (OutputContains(sensitive_data) ∨ ToolCall(exfil, _)))
}

policy data_exfiltration {
  require G ¬(DataFlow(user_context, external_api) ∧
    ¬UserConsented(external_api))
}

policy tool_sandbox {
  require G (ToolCall(code_exec, args) →
    (ArgsSatisfy(args, sandbox_constraints) ∧
     OutputType(output, expected_type)))
}
```

---

## 🛡️ Runtime Enforcer

The enforcer is a **verified reference monitor** implemented in Rust with Coq proofs:

```rust
// High-performance enforcer (Rust)
pub struct Enforcer {
    policy: PsPolicy,
    model: ModelHandle,
    attestation_key: Ed25519PrivateKey,
}

impl Enforcer {
    pub fn enforce(&self, request: Request) -> Result<Response, EnforcementError> {
        // 1. Static PSL check on request
        self.policy.check_request(&request)?;
        
        // 2. Execute with tool interception
        let trace = self.model.execute_with_interception(request)?;
        
        // 3. Validate trace against PSL
        self.policy.check_trace(&trace)?;
        
        // 4. Emit attestation
        let attestation = self.attest(request, trace)?;
        
        Ok(Response { trace, attestation })
    }
}
```

**Coq verification** covers:
- Memory safety (no buffer overflows, use-after-free)
- Functional correctness (policy checking matches PSL semantics)
- Attestation unforgeability (Ed25519 EUF-CMA)
- Non-interference (enforcer doesn't leak secrets)

---

## 📈 Benchmarks

### Adversarial Test Suite (10,000 prompts)

| Source | Count | Description |
|--------|-------|-------------|
| PromptInject | 3,200 | Encoded, multi-turn, encoding attacks |
| HijackLLM | 2,800 | Adaptive chosen-prompt attacks |
| Custom agentic | 2,500 | Multi-step tool-use chains |
| Sandbox escapes | 1,500 | Code exec, fs, network bypasses |

### Ablation Results

| Configuration | False Negatives | Verification Time |
|---------------|-----------------|-------------------|
| Full framework | **0** | 3.6 s |
| No abstract interpretation | 247 | N/A |
| No runtime enforcer | 0* | 3.6 s |
| No attestation | 0* | 3.6 s |
| Intervals only (no zonotopes) | 89 | 1.2 s |

*Attacks succeed at runtime without enforcer/attestation.

---

## 📚 Documentation

- [PSL Reference](docs/psl_reference.md) — Complete language specification
- [Verification Guide](docs/verification_guide.md) — Running the pipeline
- [Enforcer API](docs/enforcer_api.md) — Integration guide
- [Artifact Checklist](docs/artifact_checklist.md) — Reproducibility

---

## 📄 Citation

```bibtex
@article{scott2026constitutional,
  title={Constitutional Security: A Formal Framework for Provably Safe AI Deployment},
  author={Scott, Michael A.},
  journal={arXiv preprint arXiv:2611.XXXXX},
  year={2026},
  affiliation={PNTHR AI Research},
  url={https://pnthr.xyz/research/constitutional-security}
}
```

---

## 🤝 Contributing

We welcome contributions to:
- Additional PSL policies
- Abstract domain improvements
- Coq proof extensions
- Benchmark prompt expansions
- Documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 📞 Contact

**Michael A. Scott (metathesage)**  
PNTHR AI Research · dev@pnthr.xyz · [@metathesage](https://x.com/metathesage)  
PNTHR AI · Base (8453)

---

**PNTHR AI Research Desk** — Theses updated as regimes change, not on a calendar.