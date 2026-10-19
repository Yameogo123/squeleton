#!/usr/bin/env node
// PostToolUse hook: after Claude edits a TS/JS file, lint THAT file only (fast, cheap).
// Errors are sent back to Claude (exit 2) so it fixes them right away.
// Silently does nothing when dependencies aren't installed yet.
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const event = JSON.parse(readFileSync(0, 'utf8'));
const file = event.tool_input?.file_path ?? '';
if (!/\.(ts|tsx|js|jsx|mjs)$/.test(file) || !existsSync(file) || file.includes('node_modules')) process.exit(0);

const project = process.env.CLAUDE_PROJECT_DIR ?? process.cwd();
const bin = (name) => join(project, 'node_modules', '.bin', name);
const linter = ['oxlint', 'eslint'].map(bin).find(existsSync);
if (!linter) process.exit(0);

// run from the project root so the linter finds its config (eslint.config.js / .oxlintrc.json)
const result = spawnSync(linter, [file], { encoding: 'utf8', cwd: project });
if (result.status !== 0) {
  console.error(`Lint issues in ${file}:\n${(result.stdout + result.stderr).trim().slice(0, 2000)}`);
  process.exit(2);
}
