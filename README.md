<p align="center"><img src="assets/banner.svg" alt="SSH Cert Window — Inspect OpenSSH certificate validity, principals, and expiry risk using ssh-keygen." width="100%"></p>

# SSH Cert Window ✨

> Inspect OpenSSH certificate validity, principals, and expiry risk using ssh-keygen.

[![CI](https://github.com/MofidChallenge10/ssh-cert-window/actions/workflows/ci.yml/badge.svg)](https://github.com/MofidChallenge10/ssh-cert-window/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) ![Stack](https://img.shields.io/badge/Stack-Python-informational)

## 🎯 Why this project?

Inspect OpenSSH certificate validity, principals, and expiry risk using ssh-keygen. It focuses on a narrow operational problem and keeps its output inspectable, deterministic, and suitable for scripts or CI.

## 🚀 Features

- 🧭 Solves the documented use case without a hosted service.
- 🧪 Includes repeatable tests and a runnable example.
- 📄 Supports concise human-readable output; machine-readable output is available where documented.
- 🔒 Avoids changing the target system during inspection.

## ⚡ Quick Start

```bash
python -m pip install -e .
ssh-cert-window examples/sample-cert-info.txt --fixture --warn-days 14
```

## 🖥️ Example

```text
Certificate: user
Key ID: deploy-readonly
Principals: deploy, release
Valid until: 2027-01-01T00:00:00Z
Status: VALID
```

## 🗺️ Roadmap

- Add directory scanning with explicit include patterns.
- Add JSON output schema versioning.
- Add optional policy files for allowed principals and maximum lifetime.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports should include the command, a minimal input fixture, and the observed output. Please do not attach credentials or private production data.

## 📜 License

MIT — see [LICENSE](LICENSE).
