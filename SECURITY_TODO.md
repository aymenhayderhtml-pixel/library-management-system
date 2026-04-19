# SECURITY INCIDENT - Todo List
**Created:** 2026-03-15 02:58 EAT
**Status:** URGENT - Credentials exposed in audit conversation

---

## PHASE 1: IMMEDIATE DAMAGE CONTROL (Rotate All Exposed Secrets)

- [ ] **Rotate Telegram Bot Token**
  - Via @BotFather on Telegram
  - Update `openclaw.json` with new token
  - Test bot functionality

- [ ] **Rotate Gmail App Password**
  - Via Google Account Security → App passwords
  - Update `identity/email_creds.json` with new password
  - Fix malformed JSON (missing closing quote on email field)

- [ ] **Rotate AgentMail API Key**
  - Via console.agentmail.to
  - Update `openclaw.json` with new API key

- [ ] **Consider rotating Exec Approvals Socket Token** (lower risk, local only)
  - Check if rotation is possible/supported
  - Update `exec-approvals.json` if rotated

---

## PHASE 2: CONFIG HARDENING

- [ ] **Move secrets out of plaintext**
  - Research: Use environment variables or secrets manager
  - Implement secure credential storage
  - Remove secrets from `openclaw.json`

- [ ] **Fix agent-browser security**
  - Enable `--content-boundaries`
  - Configure domain allowlist

- [ ] **Review Telegram groupPolicy**
  - Change from `"open"` to restricted groups only
  - Update `openclaw.json` or relevant config

- [ ] **Consider disabling skill watch mode**
  - Evaluate if `watch: true` is necessary
  - Disable if not needed for hot-reload

---

## PHASE 3: BINARY & DEPENDENCY CHECK

- [ ] Install missing binaries if needed:
  - `nano-pdf` (pip install nano-pdf)
  - `whisper` (pip install openai-whisper)
  - `qmd` (npm install -g qmd)

---

## PHASE 4: POST-MORTEM & PREVENTION

- [ ] Review how credentials ended up in plaintext files
- [ ] Set up secret scanning / git pre-commit hooks
- [ ] Document secure credential management process
- [ ] Schedule regular security audits

---

## NOTES
- Current runtime: Step-3.5 Flash (default model: Trinity)
- All rotations should happen **before** any other work
- Test each rotation immediately after updating config
- Keep track of old tokens for revocation confirmation
