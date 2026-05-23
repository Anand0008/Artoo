# Sanitization Report

**Source:** `C:\Users\anand\Downloads\Artoo-main`
**Destination:** `C:\Users\anand\Downloads\_clean_uploads\Artoo-main`

## Summary

- 97 files copied
- 14 files deleted
- 14 files had patterns scrubbed
- 0 files kept with suspicious names (manual review recommended)

## Deleted files

- `Artoo-main\Artoo\.env` — exact-name match in DELETE_EXACT_NAMES (.env)
- `Artoo-main\Artoo\.env.backup` — exact-name match in DELETE_EXACT_NAMES (.env.backup)
- `Artoo-main\Artoo\agents\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\app_logging\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\config\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\llm\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\mcp_client\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\metrics\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\persistence\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\prompts\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\scheduler\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\schemas\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\utils\__pycache__` — dir name in DELETE_DIR_NAMES (__pycache__)
- `Artoo-main\Artoo\venv4` — contains venv marker (pyvenv.cfg)

## Scrubbed inline


### `Artoo-main\Artoo\.env.example`

- [ENV_STYLE_SECRET] `JIRA_API_TOKEN=FILL_THIS_IN`
- [ENV_STYLE_SECRET] `GITHUB_PERSONAL_ACCESS_TOKEN=FILL_THIS_IN`
- [ENV_STYLE_SECRET] `METRICS_API_KEY=local-test-key-changeme`

### `Artoo-main\Artoo\create_jiras.py`

- [EMAIL] `anandinfinity0007@gmail.com`
- [TOKEN_ASSIGN] `JIRA_TOKEN = "ATATT3xFfGF0s0z5aKeiyIi7SUVOTKlMAoJ_2sDY54beQ_mmc_edUSQ0mkE9Am79ql`

### `Artoo-main\Artoo\Dockerfile`

- [EMAIL] `contact@telomeregs.com`

### `Artoo-main\Artoo\github_project_and_confluence_setup_guide.md`

- [EMAIL] `your@email.com`
- [ENV_STYLE_SECRET] `JIRA_API_TOKEN=your-jira-api-token`
- [ENV_STYLE_SECRET] `GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here`
- [ENV_STYLE_SECRET] `METRICS_API_KEY=mysecretkey123`

### `Artoo-main\Artoo\README.md`

- [EMAIL] `you@company.com`
- [ENV_STYLE_SECRET] `OPENAI_API_KEY=sk-...`
- [ENV_STYLE_SECRET] `JIRA_API_TOKEN=your_jira_api_token`
- [ENV_STYLE_SECRET] `GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...`
- [ENV_STYLE_SECRET] `METRICS_API_KEY=your-secret-key`

### `Artoo-main\Artoo\tool_err.txt`

- [PERSONAL_PATH_WIN] `C:\Users\anand`
- [PERSONAL_PATH_WIN] `C:\Users\anand`
- [PERSONAL_PATH_WIN] `C:\Users\anand`
- [PERSONAL_PATH_WIN] `C:\Users\anand`
- [PERSONAL_PATH_WIN] `C:\Users\anand`
- [PERSONAL_PATH_WIN] `C:\Users\anand`
- [PERSONAL_PATH_WIN] `C:\Users\anand`

### `Artoo-main\Artoo\TRADEMARK.md`

- [EMAIL] `contact@telomeregs.com`

### `Artoo-main\Artoo\tests\unit\test_sanitizer.py`

- [EMAIL] `a@x.com`
- [EMAIL] `b@y.org`
- [EMAIL] `admin@corp.io`

### `Artoo-main\Artoo\utils\sanitizer.py`

- [EMAIL] `user@domain.tld`

### `Artoo-main\Artoo-Deploy\.env.example`

- [POSTGRES_URL_CRED] `postgresql://USER:PASS@`
- [POSTGRES_URL_CRED] `postgresql://artoo:artoo@`
- [ENV_STYLE_SECRET] `JIRA_API_TOKEN=FILL_THIS_IN`
- [ENV_STYLE_SECRET] `GITHUB_PERSONAL_ACCESS_TOKEN=FILL_THIS_IN`
- [ENV_STYLE_SECRET] `METRICS_API_KEY=local_test`

### `Artoo-main\Artoo-Deploy\build.py`

- [POSTGRES_URL_CRED] `postgresql://artoo:artoo@`
- [POSTGRES_URL_CRED] `postgresql://USER:PASS@`
- [POSTGRES_URL_CRED] `postgresql://artoo:artoo@`

### `Artoo-main\Artoo-Deploy\docker-compose.laptop.yml`

- [POSTGRES_URL_CRED] `postgresql://artoo:localdev@`
- [POSTGRES_URL_CRED] `postgresql://artoo:localdev@`
- [POSTGRES_URL_CRED] `postgresql://artoo:localdev@`

### `Artoo-main\Artoo-Deploy\Dockerfile`

- [EMAIL] `contact@telomeregs.com`

### `Artoo-main\Artoo-Deploy\README.md`

- [POSTGRES_URL_CRED] `postgresql://artoo_user:YOUR_PASSWORD@`

## Next step

```bash
python _github_sanitizer.py scan "C:\Users\anand\Downloads\_clean_uploads\Artoo-main" --strict
```

Must return `OK — 0 findings` before any push.
