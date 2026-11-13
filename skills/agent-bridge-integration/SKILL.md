---
name: agent-bridge-integration
description: "Design, implement, modify, or review application–Agent integrations against the Application–Agent Integration Specification. Covers application-initiated Agents and existing Agents calling application tools, including input/output, authorization, effects, and recovery. Leaves application business workflows to their owners."
---

# Integrate Agents against the specification

English | [中文译文](SKILL.zh-CN.md)

Reply in the user's language unless they explicitly request another language.

The Skill version has one source: [VERSION](VERSION). Integration requirements come only from the repository's [specification](../../docs/general-integration-contract.en.md), with its [Chinese source edition](../../docs/general-integration-contract.md) as the reference for translation discrepancies. This Skill is usage guidance, not another normative document. The specification, Skill, and reference SDK have separate versions.

## Before working

1. Locate this Skill's real directory; resolve a symlink installation first. Read `docs/general-integration-contract.en.md` or its Chinese source two levels above that real directory. Preserve the complete specification repository when installing; copying this Skill folder alone is insufficient. If the body is unavailable, obtain the matching repository edition from the user. Do not substitute this Skill, an old summary, or an SDK design for the specification.
2. Read the body's date, version, status, and sections 1–2 and 11. Identify the requested role and required capabilities. A is application-initiated, application-scoped Agent operation; B is an existing Agent calling application methods. Apply each role separately. A B-only application does not need a new Agent-control service.
3. When networking is allowed and Python 3.9+ is available, run `python3 <real-skill-directory>/scripts/check_updates.py check`. Only `notify: true` calls for an automatic notice; follow [update handling](references/updates.md). Cached metadata may still yield a due notice. Unconfigured sources, no newer release, acknowledged notices, unexpired snoozes, and ignored versions remain quiet. Check failures do not block the integration task or establish that the installed version is current. Answer explicit update questions truthfully. Without script execution or persistent local state, do not promise cross-session deduplication, replace it with reminders on every use, or create a scheduled job yourself.

## Read the applicable requirements

Cover every applicable common obligation under section 11. This table routes to the body; it does not make mandatory requirements optional or create a second specification. Read the relevant sections before editing or judging compliance.

| Work involved | Body sections |
| --- | --- |
| Data, resource references, method descriptions, real tool results | 3–6 |
| Structured model output and generation/validation guarantees | 5.1 |
| Identity, output recipients, material disclosure, sessions, concurrency, stopping | 7 |
| Delegated background work, approvals, elicitation, waiting | 7.1 |
| Main/auxiliary task time, usage, and cost constraints | 7.2 |
| Protocol/native mappings and A/B bindings | 8–9, 11 |
| Durable writes/external effects, deduplication, unknown outcomes | 4.1–4.3, 6–7 |
| Network/local connections, deployment, diagnostics, temporary data | 12–13 |
| Integration verification and compatibility claims | 14 |

Consult upstream standards at the versions and bindings specified by the body. Missing field or capability evidence remains unverified. A brand name, newer draft, or another execution path is not substitute evidence.

## Design, implementation, and review

- Honor the requested stage: discussion produces advice, review produces evidence-backed findings, and implementation changes code. This Skill grants no additional permission to publish, install updates, call paid models, or mutate production data.
- Find the real entrypoint, existing application identity/permissions, resource and method execution owners, durable result, and consumers before mapping clauses. Reuse those owners. Do not require the reference SDK, a language, new databases/services, or Qingning domain objects merely because this Skill is active.
- The application chooses required business inputs/upstream outputs, acceptance criteria, branches, and scheduling. Check whether the declared inputs/outputs, current authorization, real effects, and recovery satisfy the body. Do not automatically classify unresolved business design or implementation bugs as missing generic specification requirements.
- Reuse existing project documentation for section 11's version, role, binding, support scope, and evidence. Do not create a registry or state system for every rule.
- A review finding needs the applicable clause, real call path, and concrete counterexample. Distinguish an unimplemented existing rule, an application-owned business decision, an unverified claim, and an actual omission in the body. A claimed specification gap must explain why existing clauses are insufficient.

## Verify and deliver

Use section 14 and the actual change to select existing tests and real-entrypoint checks. Cover applicable normal and negative cases. Writes, interaction, recovery, multiple services, and network operation determine conditional coverage; do not force all optional capabilities into every application.

Report the body version, actual role/runtime combination, results, and remaining boundaries. Distinguish document declarations, source confirmation, real-path verification, and independent interoperability. One passing path does not establish all-engine or all-deployment support. Loading this Skill or successfully running its checker does not establish application conformance.

If this Skill's index or advice conflicts with the body, use the body to assess integration requirements and report the Skill discrepancy. An explicit user change of scope must be reflected honestly in the conformance report; a deviation from a MUST is not conformance.
