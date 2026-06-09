# Source-Available Licensing Options

This document is an exploratory maintainer note, not legal advice.

Gale wants to explore moving Socket from broad Apache 2.0 reuse toward a free-for-non-commercial-use model where businesses that profit from Socket, its plugins, or its skill corpus need to negotiate commercial terms.

## Current State

Socket is currently Apache 2.0 at the root.

Relevant surfaces:

- [`LICENSE`](../../LICENSE) contains Apache License 2.0.
- [`NOTICE`](../../NOTICE) says the repository is licensed under Apache License 2.0 and warns that child repositories and packaged plugin surfaces may carry their own legal surfaces.
- [`README.md`](../../README.md) says the `socket` superproject and all nested projects are Apache 2.0.
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md) says contributions are made under Apache 2.0 unless explicitly stated otherwise.
- Many `SKILL.md` files carry `license: Apache-2.0` in frontmatter.
- `plugins/apple-dev-skills/LICENSE` is also Apache 2.0.

Practical implication:

- Existing Apache 2.0 grants for already-published versions should be treated as continuing for those versions.
- A future licensing change can govern future versions only if Gale controls the required copyrights or has contributor permission to relicense.
- Before accepting outside contributions under a new commercial model, Socket needs contribution terms that preserve Gale's ability to offer commercial licenses.

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

## Candidate Models

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

The strongest first candidate is:

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

Recommended fallback:

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

- Decide whether the restriction applies to all of Socket or only selected child plugins.
- Decide whether commercial internal use, consulting use, vendor embedding, training-data use, hosted-service use, and paid courseware use are all commercial.
- Decide whether charities, educational institutions, public research organizations, government institutions, and individual contractors get noncommercial treatment.
- Decide whether old versions should ever convert back to Apache 2.0.
- Ask a lawyer to review the chosen public license and commercial-license posture before changing legal files.

### Phase 2: Prepare Repo Surfaces

- Add a new root license file for the selected public license.
- Update `NOTICE` to explain old-version Apache terms versus future-version terms.
- Update `README.md` license wording.
- Update `CONTRIBUTING.md` so contributions after the change are made under terms that allow Gale to offer commercial licenses.
- Update child plugin README or license files where they currently state Apache 2.0.
- Update `SKILL.md` frontmatter license values consistently.
- Update marketplace metadata if it carries license fields.
- Add a `COMMERCIAL-LICENSE.md` or `COMMERCIAL-USE.md` contact note with plain-language examples.

### Phase 3: Validate Tooling

- Run root metadata validation.
- Run child validation for any plugin whose frontmatter or metadata changed.
- Install-test the Socket marketplace with the changed metadata in a temporary `CODEX_HOME`.
- Confirm Codex still displays or installs the plugins without license-field assumptions breaking.

### Phase 4: Release

- Treat the licensing change as a major or at least clearly called-out release.
- Tag the last Apache 2.0 version clearly before the license change.
- Publish release notes that explain the first version under the new license.
- Preserve archived Apache 2.0 terms for old versions.

## Commercial-Use Questions To Answer

- Does a developer using Socket at work for their employer count as commercial use?
- Does an independent contractor using Socket for a paid client count as commercial use?
- Does a company using Socket internally without redistributing it count as commercial use?
- Does a startup prototype count as commercial use before revenue?
- Does a paid course, book, or training program using Socket examples count as commercial use?
- Does training or evaluating commercial AI systems on Socket skill content count as commercial use?
- Does Apple, OpenAI, Anthropic, Microsoft, or another vendor using Socket ideas, skills, or plugin content in product work require a commercial license?

The answers should be written before the license changes so users do not have to infer Gale's intent.

## Initial Commercial-Use Draft Language

This is not final legal text.

```text
Socket is free for personal, hobby, educational, research, public-interest, and other noncommercial use under the public license for this version.

Commercial use requires a separate written license from Gale. Commercial use includes using Socket, its plugins, skills, documentation, examples, prompts, MCP servers, hooks, or packaged artifacts for a business, employer, client, paid product, hosted service, commercial training, paid consulting, product development, or other activity intended to generate revenue, reduce business costs, or provide commercial advantage.

For commercial licensing, contact Gale W at mail@galewilliams.com.
```

## Decision Checklist

- [ ] Decide whether to use PolyForm Noncommercial, BSL, FSL, or another lawyer-reviewed source-available license.
- [ ] Decide whether the license change applies to all child plugins at once.
- [ ] Decide whether to keep `apple-dev-skills` in lockstep with Socket.
- [ ] Decide whether to require a CLA, DCO plus outbound license grant, or another contribution term before accepting outside contributions.
- [ ] Decide whether to tag one final Apache 2.0 release before the switch.
- [ ] Run install testing before publishing the changed marketplace.
