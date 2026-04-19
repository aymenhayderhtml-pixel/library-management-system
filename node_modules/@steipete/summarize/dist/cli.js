#!/usr/bin/env node
if (!process.env.SUMMARIZE_GIT_SHA) process.env.SUMMARIZE_GIT_SHA = "ae52818b"
await import('./esm/cli.js')
