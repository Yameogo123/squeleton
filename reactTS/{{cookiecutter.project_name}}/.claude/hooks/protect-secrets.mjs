#!/usr/bin/env node
// PreToolUse hook: never let Claude read, print, edit or grep secret files.
// Exit code 2 blocks the tool call and shows the reason to Claude.
// Templates such as .env.example / .env.template stay readable (they hold no values).
import { readFileSync } from 'node:fs';

const ALLOWED = /\.env\.(example|template|sample|dist)$/;
const SECRET = new RegExp(
  String.raw`(?:(?<=[\\/\s'"=])|^)(` +
    String.raw`\.env(\.[\w.-]+)?` +
    String.raw`|[\w.-]+\.(pem|key|p8|p12|pfx|jks|keystore|mobileprovision)` +
    String.raw`|id_(rsa|ed25519|ecdsa)[\w.-]*` +
    String.raw`|credentials\.json|service-account[\w.-]*\.json|google-services\.json|GoogleService-Info\.plist` +
    String.raw`)(?=$|[\s'";|&)<>])`,
  'g',
);

function secretIn(text) {
  for (const match of ` ${text ?? ''} `.matchAll(SECRET)) {
    if (!ALLOWED.test(match[1])) return match[1];
  }
  return null;
}

const event = JSON.parse(readFileSync(0, 'utf8'));
const input = event.tool_input ?? {};
const candidates =
  event.tool_name === 'Bash'
    ? [input.command]
    : ['file_path', 'path', 'notebook_path', 'glob'].map((k) => input[k]); // Grep's search pattern is not checked

for (const text of candidates) {
  const hit = secretIn(text);
  if (hit) {
    console.error(
      `Blocked by .claude/hooks: '${hit}' is a secrets file. Do not read, print, copy or edit it. ` +
        'Use .env.example for variable names, and ask the user to set values.',
    );
    process.exit(2);
  }
}
