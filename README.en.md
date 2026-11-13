# Agent Bridge Spec

English | [中文](README.md)

An application–Agent integration specification, with reference SDK design and integration examples, for user-owned local or remote Agents. Applications may use the reference SDK or implement the same specification independently. End users connect, authorize, and perform tasks in integrated applications or their original Agent hosts.

Official repository: [alcheme-labs/agent-bridge-spec](https://github.com/alcheme-labs/agent-bridge-spec). `local-agent-bridge` is the local directory name; integrations are not limited to local Agents. Since 2026-11-12 this directory is the project's main home. Historical ResearchStudio copies are no longer synchronized.

## Current status

Updated 2026-11-13. Deliverables include product/specification documents, the bilingual specification, reference implementation design, and companion Skill source `0.1.0`. The Bridge runtime has not been developed, extracted from Qingning, built, published, or runtime/interoperability-tested, and there is no installable public SDK package. The Skill is distributed through independent GitHub Releases; consult the [release records](https://github.com/alcheme-labs/agent-bridge-spec/releases) for published versions and release verification. Both the official repository and update source are `alcheme-labs/agent-bridge-spec`.

The specification is **normative draft 0.3** and the SDK is **reference design draft 0.3**. This revision adds delegated background decisions, structured-output guarantees, and main-task time/budget rules, retaining the prior specification/SDK separation and safety/recovery requirements. Consumer business responsibilities remain separate.

The [draft 0.2 gap review](docs/reviews/2026-11-13-normative-gap-review.md) records two closed P2 document findings for that version, not this revision. The [draft 0.3 runtime-rules review](docs/reviews/2026-11-13-runtime-rules-review.md) records independent reviewers and a final judge finding no material document issue. Neither conclusion is runtime compatibility evidence. Actual first engine/host/connection products, a second real consumer, independent runtime integration, reference SDK distribution, and licensing review for future extracted code remain outstanding.

The [2026-11-12 specification review](docs/reviews/2026-11-12-spec-review.md) and [2026-11-02 protocol review](docs/reviews/2026-11-02-protocol-review.md) retain their historical scope; they do not automatically approve newer versions.

## Documents and responsibilities

| Document | Maintained responsibility |
| --- | --- |
| [Product specification](SPEC.md) | Goals, actors, complete user paths, deliverables, exit gates |
| [Integration specification, English](docs/general-integration-contract.en.md) / [Chinese source](docs/general-integration-contract.md) | The single specification's language editions: implementation-independent obligations, bindings/capabilities, permissions/effects, recovery, security/privacy, conformance. Matching versions/numbers; resolve translation discrepancies against the Chinese source |
| [Reference SDK/Qingning design](docs/sdk-and-qingning-integration-design.md) | One Node/TypeScript implementation design, host/engine/tool boundaries, extraction and compatibility facts; not mandatory interfaces for independent implementations |
| [Integration Skill](skills/agent-bridge-integration/SKILL.md) / [Chinese translation](skills/agent-bridge-integration/SKILL.zh-CN.md) | AI guidance for implementation/review against the body, responding in the user's language; no new business or normative rules |
| [Previous gap review](docs/reviews/2026-11-13-normative-gap-review.md), [runtime-rules review](docs/reviews/2026-11-13-runtime-rules-review.md) | Version-scoped decisions, checks, and unexecuted runtime boundaries |
| [ServerAgent expectations](docs/serveragent-expectations.md) | Original consumer input. Three generic semantic groups were adopted; specific non-Node/SDK integrations, business responsibilities, and runtime support are not delivered |
| [Extraction assessment](docs/extraction-assessment.md) | 2026-11-04 source facts and extraction/retention assessment |
| [Validation/progression plan](docs/validation-plan.md) | Historical reuse/contribution/selection research, not current normative or delivery status |
| [Positioning](docs/product-positioning.md), [features/flows](docs/v1-features-and-flows.md) | Actor/scenario/operation baselines, subject to the specification body |

Read product goals first, then the integration body. SDK design is relevant when adopting/developing that implementation. Historical evidence is not current verification. Adopting generic ServerAgent semantics does not deliver every requested combination or move its service contract, candidate acceptance/activation, or maintenance queue into Bridge. Supporting historical/design documents remain in their original language.

## Product boundaries

- A uses one's Agent inside the application; B calls the application from an existing Agent. Both reuse original business methods/permissions and have separate acceptance. B need not install a second service controlling the whole Agent.
- New/existing applications share the specification. Application authors integrate first; users then connect/authorize. Installing a connector alone cannot give a closed application missing business capabilities.
- Qingning is source practice and the first reference-SDK consumer. Its identity, permissions, scheduling, data, and installation stay with their owners. Other applications do not depend on Qingning accounts, servers, or domain models.
- Reuse ACP, MCP, or documented native mappings. Add no general RPC, business database, identity center, or competing transcript owner.
- Preserve local/remote, complete-output, write/readback, and safe-recovery goals. Runtime-only, read-only, or single-combination demonstrations report only their actual scope.
- Bridge runtime development remains deferred. This authorized work adds only the Skill, its local update checker, and language editions. Later runtime work first verifies trustworthy write correlation, response loss, and original-owner deduplication before authorized implementation/compatibility work.

## Companion Skill

`skills/agent-bridge-integration/VERSION` is the sole Skill version source, currently `0.1.0`, independently versioned from normative draft 0.3. English `SKILL.md` is the discovery entrypoint; the Chinese file is a corresponding translation. Both require replies in the user's language.

Install using the complete repository layout and let the host read `skills/agent-bridge-integration`. Hosts supporting symlinks may link that real directory. Resolve the actual directory to read the matching body without another maintained specification copy. Copying just the Skill folder is insufficient. There is no separately published Skill installer/package; this work does not change locally installed Skills.

For the initial version, use the [complete source package with license files](https://github.com/alcheme-labs/agent-bridge-spec/releases/download/agent-bridge-integration-v0.1.0/agent-bridge-spec-0.1.0.tar.gz). The original release tag predates the licensing supplement and remains unchanged. Its specification and Skill can also be obtained below; license files are available separately on the same Release:

```sh
git clone --branch agent-bridge-integration-v0.1.0 https://github.com/alcheme-labs/agent-bridge-spec.git
```

Checks run on activation and normally reuse network results for 24 hours. Each newer version is automatically shown once after display acknowledgement. Ignore and snooze decisions persist outside the repository in user-local state, coordinated with file locks and atomic writes. Cache use does not suppress a due notice; follow `notify`. The helper never installs updates; explicit consent is required. There is no resident process or promise to check while the Skill is inactive.

`repository` in `update-source.json` is configured as `alcheme-labs/agent-bridge-spec`. Publish Skill releases using independent tags such as `agent-bridge-integration-v0.1.0` as GitHub Releases, with actual change notes. Pushing code or creating an ordinary Git tag alone does not trigger Skill update notices. See [update/state handling](skills/agent-bridge-integration/references/updates.md).

The checker uses only Python 3.9+ standard-library modules. Local verification:

```sh
python3 -B -m unittest discover -s tests -p 'test_skill_updates.py' -v
python3 skills/agent-bridge-integration/scripts/check_updates.py check
```

On 2026-11-13, all 31 local checks, Skill structure validation, relative-link checks, and code syntax checks passed. Independent behavioral verification and bilingual specification fidelity review were completed. The original Chinese clauses are unchanged apart from language navigation/edition notes. Tests use temporary local state and simulated GitHub responses, including real cross-process locking, CLI execution, and truncated HTTP byte streams. They do not establish official-repository online checks or Bridge/application interoperability.

Online verification must read actual published releases and separately check the installed version, newer-version detection for an older installation, and local notification deduplication. Each Release's notes record its actual online results; passing local tests alone does not establish a successful online check.

Maintainers can manually run [Verify published Skill](https://github.com/alcheme-labs/agent-bridge-spec/actions/workflows/verify-skill-release.yml) against the specified newest published tag in an isolated environment. Alternatively run `python3 -B tests/verify_skill_updates_online.py`. It uses the anonymous API and temporary state, simulates an older version, and neither installs updates nor modifies published source. This requires network access and is separate from the default offline tests.

## License

This repository's original documents (including both specification editions), Skill, and maintenance tools use the [Apache License 2.0](LICENSE), including the published Skill `0.1.0` contents. See [NOTICE](NOTICE) for copyright and third-party reference information. The standard license text is in English; project explanations are maintained in both languages.

Referenced third-party standards and projects retain their own licenses. Any future extraction of third-party implementations requires a separate licensing and attribution review.

## Maintenance

- Maintain integration obligations in the specification, product goals in SPEC, and implementation choices in SDK design. Summaries/examples cannot omit mandatory safeguards/acceptance.
- This directory is the maintained project home; ResearchStudio retains historical copies rather than another live definition.
- Product definition, normative rules, implementation design, code, and runtime acceptance remain distinct. A document is not delivered implementation.
- Use relative links; date/version external source evidence without depending on the author's local paths. Do not rewrite historical review conclusions as approval of later revisions.
- Do not include real credentials or private configuration. Check source, attribution, and authorization before extracting third-party code; do not automatically extend this repository's license to third-party material.
