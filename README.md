## Run with Docker Compose

Start the application:

```bash
docker compose up -d


##DevSecOps Security Scanning

This project includes a DevSecOps security workflow using GitHub Actions.

The security workflows runs on every push and pull request to the "main" branch.

### Security Tools Used

Gitleaks | Scans the repository for accidentally committed secrets|
Trivy | Scans the filesystem and Docker image for vulnerabilities |
Checkov | Scans configuration and Infrastructure-as-Code files for misconfigurations |

### Security Workflow

'''text
Push or pull request
   ↓
Gitleaks secret scan
   ↓
Trivy filesystem scan
   ↓
Docker image build
   ↓
Trivy container image scan
   ↓
Checkov configuration scan
-note: Checkov currently configured with soft_fail: true because the project does not yet include Terraform or Kubernetes files.
This can be changed to fail the workflow when misconfigurations are found.
