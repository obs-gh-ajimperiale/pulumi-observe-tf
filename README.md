# Pulumi + Observe Monitor Example (via Terraform Bridge)

This project demonstrates how to provision an `observe_monitor_v2` resource in [Observe](https://www.observeinc.com) using [Pulumi](https://www.pulumi.com/) and the [Pulumi Terraform Bridge](https://www.pulumi.com/blog/terraform-bridge-provider/).

It uses the official `observeinc/observe` Terraform provider, bridged into Pulumi and used from Python code.

---

## 📦 Prerequisites

- [Pulumi CLI](https://www.pulumi.com/docs/install/)
- Python 3.8+
- `virtualenv` or another virtual environment tool
- An Observe account with either:
  - User email and password, or
  - API token
  - customerID

---

## 🛠️ Setup (Steps 1–3)

> Use this exact block to get started quickly in a fresh directory.

```bash
# 1. Create a new Python-based Pulumi project
pulumi new python

# 2. Add the Terraform Observe provider using the Pulumi Terraform Bridge
pulumi package add terraform-provider registry.terraform.io/observeinc/observe

# 3. Install the generated SDK locally
pip install -e ./sdks/observe
```

---

## 📁 Project Files

- `provider.py` – Authenticates to the Observe provider using hardcoded credentials (can be refactored to use secrets). Insert appropriate CustomerID, Domain, user_email, and user_password
- `main.py` – Defines and provisions a usage-based `observe_monitor_v2` from the Observe Usage Metrics dataset.
