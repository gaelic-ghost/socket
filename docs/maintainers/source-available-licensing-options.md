# Source-Available Licensing Options

This document is a maintainer note, not legal advice.

Gale decided to move future Socket versions from broad Apache 2.0 reuse toward a free-for-non-commercial-use model where businesses that profit from Socket, its plugins, or its skill corpus need to negotiate commercial terms.

## Current State

Socket is currently PolyForm Noncommercial 1.0.0 at the root for future public versions.

Relevant surfaces:

- [`LICENSE`](../../LICENSE) contains PolyForm Noncommercial 1.0.0.
- [`COMMERCIAL-USE.md`](../../COMMERCIAL-USE.md) states the commercial-use policy and contact path.
- [`NOTICE`](../../NOTICE) includes Socket's PolyForm `Required Notice:` line.
- [`README.md`](../../README.md) says the `socket` superproject and nested projects are PolyForm Noncommercial 1.0.0 for future public versions.
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md) says contributions are made under PolyForm Noncommercial 1.0.0 unless explicitly stated otherwise, and calls out that Gale may offer separate commercial licenses.
- `SKILL.md` files should carry `license: PolyForm-Noncommercial-1.0.0` in frontmatter when they belong to this licensing surface.
- `plugins/apple-dev-skills/LICENSE` is also PolyForm Noncommercial 1.0.0.
- [`LICENSE-HISTORICAL-APACHE-2.0`](../../LICENSE-HISTORICAL-APACHE-2.0) preserves the historical Apache 2.0 text for previously published Apache-licensed versions.

Practical implication:

- Existing Apache 2.0 grants for already-published versions should be treated as continuing for those versions.
- A future licensing change can govern future versions only if Gale controls the required copyrights or has contributor permission to relicense.
- Before accepting outside contributions under this commercial model, Socket needs contribution terms that preserve Gale's ability to offer commercial licenses.

## Licensing Goal

The target posture is:

- Free personal, hobby, educational, public-interest, and noncommercial use.
- Source-visible development.
- Commercial users must negotiate with Gale before using Socket or its child plugins for business benefit.
- Gale can still publish commercial licenses directly.
- The public license should not accidentally allow a commercial platform, tool vendor, consultancy, courseware business, or internal enterprise agent program to profit from Socket without a separate agreement.

## Constraints

- This will no longer be open source under the Open Source Definition if commercial use is restricted. OSI's Open Source Definition requires free redistribution without royalties or fees and does not allow field-of-use discrimination.
- Creative Commons itself recommends against using Creative Commons licenses for software. It can still be useful for non-code documentation or media, but it is a poor fit for source code and executable plugin behavior.
- Some package ecosystems, contributors, companies, and dependency scanners reject non-open-source or source-available licenses by policy.
- Current Codex plugin marketplace behavior may expect license metadata to be simple. Any license metadata changes need install testing.
- Child surfaces may need different migration timing. `apple-dev-skills` has its own `LICENSE` and README wording, while other child plugins mostly rely on root legal surfaces plus `SKILL.md` frontmatter.

## Candidate Models Considered

### Option A: PolyForm Noncommercial With Commercial Licenses

Use [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/) for future public Socket versions, and offer separate commercial licenses by negotiation.

Why it fits:

- It is designed for software.
- It grants broad rights for permitted noncommercial purposes.
- It has explicit patent-license and violation-cure terms.
- It clearly says commercial use is not included unless separately licensed.

Tradeoffs:

- It is not open source.
- "Noncommercial" still requires interpretation at the edge.
- Some businesses may reject it automatically.
- Existing Apache 2.0 versions remain available under Apache 2.0.

Best fit:

- Socket wants a simple, clear, future-only noncommercial default.
- Gale wants commercial negotiation without a mandatory delayed open-source conversion.

### Option B: Business Source License 1.1 With A Narrow Free Grant

Use [Business Source License 1.1](https://mariadb.com/bsl11/) for future public versions, with an Additional Use Grant that permits noncommercial, educational, personal, or public-interest use, and requires commercial licenses for production or business-profit use.

Why it fits:

- It is software-specific and commonly understood as source-available.
- It explicitly says users must buy a commercial license or stop using the work if their use is outside the license.
- It has a built-in future Change License path.

Tradeoffs:

- It is more complex than PolyForm Noncommercial.
- It requires choosing a Change Date and Change License.
- The mandatory future open-source conversion may not match Gale's goal if the paid boundary should remain permanent.
- Each Additional Use Grant creates project-specific interpretation work.

Best fit:

- Socket wants delayed open-source conversion after a fixed window.
- Gale wants enterprise users to negotiate during the protected window.

### Option C: Functional Source License

Use [Functional Source License](https://fsl.software/) if the goal is a standardized fair-source model that converts each version to Apache 2.0 or MIT after two years.

Why it fits:

- It is designed for source-available software with delayed permissive licensing.
- It tries to be less variable than BSL.
- It may feel familiar to companies watching newer fair-source projects.

Tradeoffs:

- It is optimized for protecting producers from direct competition or harmful free-riding, not purely for "all commercial users must negotiate."
- It converts to Apache 2.0 or MIT after two years.
- It may not block as many internal commercial uses as Gale wants, depending on final license terms.

Best fit:

- Socket wants a fair-source posture where old versions become permissive.
- Gale is comfortable with some commercial internal use that does not undermine Socket.

### Option D: Apache 2.0 Core Plus Commercial Add-Ons

Keep core Socket under Apache 2.0, then move premium assets, hosted services, templates, packaged Xcode plug-ins, enterprise guidance, or automation services under commercial terms.

Why it fits:

- It preserves open-source adoption.
- It avoids relicensing friction for existing users.
- It is easiest for contributors and automated tools.

Tradeoffs:

- It does not stop businesses from profiting from the public skill corpus.
- It only monetizes separate premium surfaces.
- It may be too weak if the concern is Apple or other vendors absorbing the core ideas.

Best fit:

- Socket primarily wants reach, community trust, and broad reuse.
- Commercial value can live in private support, hosted services, or proprietary companion tooling.

### Option E: Dual License With A Custom Commercial Agreement

Publish future Socket versions under a noncommercial public license and offer commercial licenses directly from Gale.

This is not a separate public license choice. It is the business model layered over Option A, B, or C.

Why it fits:

- It matches the desired negotiation path.
- It lets Gale price by business use case.
- It keeps personal use free.

Tradeoffs:

- Contribution terms must give Gale the right to relicense contributions commercially.
- The commercial agreement needs lawyer review.
- Public docs need clear contact and permitted-use language.

Best fit:

- This should likely be paired with PolyForm Noncommercial if the public license should be simple and permanent.

## Recommendation

The chosen model is:

```text
Future public versions: PolyForm Noncommercial 1.0.0
Commercial use: separate commercial license from Gale
Existing versions: remain under their previously published Apache 2.0 terms
```

Reason:

- It most directly matches "free for noncommercial use; businesses negotiate."
- It avoids BSL/FSL's delayed conversion if Gale does not want old versions to become permissive automatically.
- It is designed for software, unlike Creative Commons NonCommercial.
- It keeps the first migration understandable.

Fallback considered:

```text
Future public versions: Business Source License 1.1
Additional Use Grant: personal, educational, public-interest, and noncommercial use
Change License: Apache 2.0
Change Date: 4 years from each version publication, or a shorter window if Gale prefers
Commercial use: separate commercial license from Gale
```

Use this only if a delayed open-source conversion is desirable.

## Migration Plan

### Phase 1: Decide Policy

- [x] Decide whether the restriction applies to all of Socket or only selected child plugins.
- [x] Decide whether commercial internal use, consulting use, vendor embedding, training-data use, hosted-service use, and paid courseware use are all commercial.
- [x] Decide whether contractors, employees working for employers, startups, businesses training models, and nonprofits doing commerce are commercial.
- [x] Decide whether charities, educational institutions, public research organizations, and government institutions need narrower repo-specific clarification beyond PolyForm's permitted-use text.
- [x] Decide whether old versions should ever convert back to Apache 2.0.
- [ ] Ask a lawyer to review the chosen public license, commercial-use policy, and commercial-license posture before relying on it for enforcement, paid licensing negotiations, or outside-contribution intake.

### Phase 2: Prepare Repo Surfaces

- [x] Add a new root license file for the selected public license.
- [x] Update `NOTICE` to explain old-version Apache terms versus future-version terms.
- [x] Update `README.md` license wording.
- [x] Update `CONTRIBUTING.md` so contributions after the change are made under terms that allow Gale to offer commercial licenses.
- [x] Update child plugin README or license files where they currently state Apache 2.0.
- [x] Update `SKILL.md` frontmatter license values consistently.
- [x] Update marketplace metadata if it carries license fields.
- [x] Add a short `COMMERCIAL-USE.md` contact note for commercial licensing.

### Phase 3: Validate Tooling

- [x] Run root metadata validation.
- [x] Run child validation for any plugin whose frontmatter or metadata changed.
- [x] Install-test the Socket marketplace with the changed metadata in a temporary `CODEX_HOME`.
- [x] Confirm Codex still displays or installs the plugins without license-field assumptions breaking.

### Phase 4: Release

- [x] Treat the licensing change as a clearly called-out release.
- [ ] Identify the last Apache 2.0 release tag in this maintainer note.
- [x] Publish release notes that explain the first version under the new license.
- [x] Preserve archived Apache 2.0 terms for old versions.

## Commercial-Use Questions To Answer

- A developer using Socket at work for their employer is commercial use, whether or not the employer explicitly approved that use.
- An independent contractor, freelancer, consultant, sole proprietor, agency, or studio using Socket for paid services or a paid client is commercial use.
- A company using Socket internally without redistributing it is commercial use.
- A startup using Socket before or after revenue is commercial use.
- A paid course, book, training program, workshop, or consulting engagement using Socket examples or Socket-derived material is commercial use.
- A business training, evaluating, benchmarking, designing, or improving commercial AI systems, software, developer tools, agents, models, products, services, or workflows using Socket skill content is commercial use.
- A nonprofit, charity, foundation, trade group, association, or similar organization using Socket to provide services, sell work, run operations, support paid programs, reduce organizational costs, or otherwise conduct commerce is commercial use.
- Apple, OpenAI, Anthropic, Microsoft, or another vendor using Socket content, skills, examples, prompts, metadata, plugin code, or packaged artifacts in product work requires a commercial license.

The answers should be written before the license changes so users do not have to infer Gale's intent.

## Initial Commercial-Use Draft Language

This earlier draft was superseded by the shorter contact-oriented note in [`COMMERCIAL-USE.md`](../../COMMERCIAL-USE.md). It remains here as historical planning context and should not be treated as the active public text.

```text
Socket is free for personal, hobby, educational, research, public-interest, and other noncommercial use under the PolyForm Noncommercial License 1.0.0.

Commercial use requires a separate written license from Gale. Commercial use includes using Socket, its plugins, skills, documentation, examples, prompts, MCP servers, hooks, or packaged artifacts for a business, employer, client, paid product, hosted service, commercial training, paid consulting, product development, or other activity intended to generate revenue, reduce business costs, or provide commercial advantage.

For commercial licensing, contact Gale W at mail@galewilliams.com.
```

## Decision Checklist

- [x] Decide whether to use PolyForm Noncommercial, BSL, FSL, or another lawyer-reviewed source-available license.
- [x] Decide whether the license change applies to all child plugins at once.
- [x] Decide whether to keep `apple-dev-skills` in lockstep with Socket.
- [ ] Decide whether to require a CLA, DCO plus outbound license grant, or another contribution term before accepting outside contributions.
- [ ] Identify the last Apache 2.0 release tag in this maintainer note.
- [x] Run install testing before publishing the changed marketplace.
