# NetGuardian — Terms of Use & Acceptable Use Policy

*This document is a template for the NetGuardian project's maintainers to review — ideally with qualified legal counsel — before relying on it. It is **not legal advice**. It sets out conduct expectations and disclaimers that **supplement but do not modify** the GNU General Public License v3.0 (GPL-3.0) under which NetGuardian is distributed. Every item in `[square brackets]` is a placeholder to complete.*

**Effective date:** `[effective date]`
**Applies to:** the NetGuardian software, catalog data, and documentation ("NetGuardian", "the Project", "the Software"), maintained by the project maintainers ("the Maintainers") and published at `https://github.com/BladeIV/Cybersec-Framework`.

---

## Not Legal Advice (Template Notice)

This document is a **starting-point template** provided for the convenience of the Maintainers and users. It is **not legal advice**, has **not** been reviewed by a lawyer on your behalf, and creates no attorney–client relationship. Laws differ by country, state, industry, and contract, and this text has not been tailored to any of them. Before relying on it, the Maintainers should have it reviewed and adapted by **qualified legal counsel**, and you remain responsible for understanding the rules that apply to you.

Text in `[square brackets]` — for example `[governing jurisdiction]`, `[contact email]`, and `[security contact email]` — is a placeholder the Maintainers must complete. These Terms intentionally name **no** real company, address, or court.

## The Short Version

A quick summary — the sections below are what actually governs.

- **Lawful, authorized use only.** Use NetGuardian and anything it links to only on systems you **own** or have **prior written permission** to test.
- **No black-hatting.** No unauthorized access, no malice, no crime. The Maintainers do **not** condone misuse.
- **NetGuardian performs no attacks.** It is a catalog and local workflow aid that links to third-party tools — each with **its own license and terms**.
- **The tools are dual-use.** The same capability that defends a system can be misused to attack one; that line is yours to stay on.
- **You are responsible** for the laws that apply to you.
- **Found a vulnerability?** Please disclose it responsibly.
- **No warranty, no liability.** The Software is provided **"as is"**, consistent with GPL-3.0 Sections 15 and 16.
- **Separate from the license.** These conduct rules do **not** change the GPL-3.0 that governs the code.

## Acceptance of These Terms

These Terms describe the **conduct the Maintainers expect** of anyone who uses NetGuardian and the **disclaimers** under which it is offered. By downloading, installing, running, or building on NetGuardian, you ("you", "the User") acknowledge that you have read and understood them and agree to use the Software accordingly. **If you cannot use NetGuardian lawfully and with authorization, do not use it.**

These Terms govern your **conduct** and the Maintainers' **disclaimers only**. They are **not** a software license and are **separate from, and do not modify, limit, or add conditions to**, the GPL-3.0 (see *Relationship to the GPL-3.0 License*). Nothing here requires you to accept a contract in order to receive, run, study, modify, or redistribute the Software — those rights come from the GPL-3.0. *(Maintainers: confirm this framing with counsel.)*

## Definitions

- **"The Maintainers"** — the individual(s) and contributors who publish and maintain the Project.
- **"Software" / "NetGuardian" / "the Project"** — the NetGuardian program, its source code, catalog data, documentation, and local triage workspace, as distributed by the Maintainers.
- **"Catalogued Tools" / "Third-Party Tools"** — the independent, third-party security tools that NetGuardian references, links to, describes, or helps you launch. These are **not** part of NetGuardian and are **not** distributed by the Maintainers.
- **"Target"** — any system, network, account, device, application, data store, or asset you interact with, assess, scan, test, or attempt to access.
- **"Authorization"** — documented, lawful permission to act against a specific Target (see *Authorization & Written-Permission Requirement*).
- **"Rules of Engagement" (RoE)** — the agreed scope, methods, timing, and limits of an authorized engagement.
- **"Responsible / Coordinated Disclosure"** — privately reporting a discovered vulnerability to the affected party and allowing reasonable time to remediate before any public disclosure.

## What NetGuardian Is — and Is Not

NetGuardian is a **catalog and a local workflow aid** — nothing more.

- **It is a catalog.** It organizes information about 50+ freely available security tools, mapped to **NIST CSF 2.0**, with links and metadata, for browsing and filtering.
- **It is a triage workspace.** It helps you organize an **authorized** incident-response or penetration-testing case — checklists mapped to NIST CSF 2.0, notes, and a Markdown report.
- **It performs no attacks.** NetGuardian does **not** scan, exploit, or access any Target on your behalf. It opens links and helps you keep your work organized; **you** run the actual tools, with tools you control, against Targets you choose. You are solely responsible for those actions and their consequences.
- **It is a downloadable program, not a hosted service.** The Maintainers do not operate a server on your behalf, do not process your Targets or results, and have no visibility into how, where, or against what you use it.
- **It collects no data.** NetGuardian has no telemetry and does not "phone home." Case data and notes stay local on your machine. *(Maintainers: confirm this remains accurate for every release.)*
- **It does not bundle or distribute the tools.** NetGuardian links to and describes independent Third-Party Tools; it does not include, bundle, endorse, or distribute them. Each is governed by its **own license and terms** (see *Third-Party Tools & Their Licenses*).
- **The tools are dual-use.** The same capabilities that defend systems can be misused to attack them. NetGuardian is published for the **defensive, research, educational, and authorized-testing** side of that line.

## Eligibility

*(Maintainers: this section conditions use and should be confirmed with counsel.)* You may use NetGuardian only if you:

- are of legal age and capacity to form a binding agreement in your jurisdiction (or have verifiable consent from a parent or legal guardian);
- are not barred from using the Software or the Catalogued Tools under any applicable law, regulation, export control, or sanctions programme; and
- have the authority to accept these Terms, whether on your own behalf or on behalf of an organization you represent.

## Acceptable Use

The Catalogued Tools are **dual-use**. You may use NetGuardian and anything it references **only** for lawful, legitimate, and explicitly authorized purposes, including:

- **defensive security operations ("blue team")** on systems you own or administer;
- **penetration testing, red-teaming, or security research** that you are **explicitly authorized** to perform;
- **incident response and digital forensics** on systems and data you are permitted to handle;
- **education, training, and research** conducted lawfully — for example, on your own equipment, in isolated lab environments, or on deliberately vulnerable practice targets provided for that purpose.

In all cases you must act within applicable law, any contract or policy that binds you, and the Authorization and Rules of Engagement for the work.

## Authorization & Written-Permission Requirement

Before you scan, test, assess, access, or attack **any** Target, you must have **one** of the following:

1. **Ownership or full administrative control** of the Target; **or**
2. **Prior written permission** from the party empowered to grant it, obtained **before** any testing begins and defining at minimum:
   - the specific **in-scope Targets** (hosts, IP ranges, domains, applications, accounts) and anything explicitly **out of scope**;
   - the **permitted methods** and any explicitly **excluded** activities (for example, denial-of-service, social engineering, or physical access);
   - the **time window** for the work;
   - **data-handling** rules (what may be accessed, copied, stored, for how long, and how it is disposed of);
   - **points of contact**; and
   - **stop and escalation conditions** (for example, on evidence of a prior breach, third-party or customer data, or safety-critical systems).

Keep the Authorization and Rules of Engagement on record for the duration of the work and afterward as required. Verbal "go-aheads," assumed consent, a system that merely "looked open," and permission from someone who does not own or control the asset are **not** Authorization. **If you are unsure whether you are authorized, you are not — stop and obtain written permission first.**

## Prohibited Uses

You must **not** use NetGuardian, its triage workspace, or any Catalogued Tool reached through it to do, attempt, assist, or encourage any of the following:

- **Unauthorized access** — accessing, probing, scanning, enumerating, or testing any Target you do not own or lack explicit Authorization to test.
- **Exceeding or continuing past scope** — acting outside the agreed Rules of Engagement, or continuing after Authorization is withdrawn or expires.
- **Malicious code** — developing, deploying, or operating malware, ransomware, spyware, backdoors, botnets, or command-and-control infrastructure against systems you are not authorized to test.
- **Data theft or misuse** — exfiltrating, copying, selling, publishing, destroying, altering, or retaining data you are not authorized to access or keep.
- **Fraud and deception** — phishing, credential theft, identity theft, financial fraud, extortion, or impersonation outside an authorized, scoped engagement.
- **Disruption** — denial-of-service (DoS/DDoS), flooding, resource exhaustion, data destruction, tampering, or any interference with the availability or integrity of services you are not authorized to test.
- **Surveillance and harassment** — stalking, doxxing, non-consensual monitoring, harassment, or intimidation of any person.
- **Circumventing protections** — defeating access controls, authentication, encryption, licensing, or technical protection measures without Authorization.
- **Violating third-party terms** — breaching the licenses, terms of service, or acceptable-use policies of any Catalogued Tool, platform, or provider.
- **Breaking the law** — any use that violates applicable laws, regulations, sanctions, or export controls (see *Compliance with Laws, Export Controls & Sanctions*).
- **Helping others** — facilitating, instructing, or assisting anyone else in any of the above.

Using NetGuardian grants you **no** permission over any Target; permission must come from the Target's owner.

## We Do Not Condone Misuse

The Maintainers build NetGuardian for defenders, authorized testers, researchers, and students who do this work lawfully and ethically. The Maintainers **do not condone, support, assist, or accept any responsibility for** unauthorized, malicious, or criminal use of NetGuardian or anything it links to. Using this Project for "black-hat" hacking, or to harm people or systems you have no right to touch, is a misuse of it and, in most places, a crime. **Don't.**

The Maintainers may, at their discretion, decline to provide support, reject or revert contributions, and report activity they reasonably believe to be unlawful. *(Note: these Terms do not purport to terminate or revoke your rights in the Software under the GPL-3.0; see the next section.)*

## Third-Party Tools & Their Licenses

NetGuardian **catalogues and links to independent Third-Party Tools; it does not include, bundle, endorse, or distribute them.** Inclusion in the catalog is **not** an endorsement of any particular use, a warranty of fitness or safety, or a grant of any right to use that tool. Each Catalogued Tool:

- is the property of its own authors and is governed by its **own license and terms**, which you must read and comply with;
- may carry its own cost, warranty, privacy, and acceptable-use conditions (including free community editions of proprietary products, each labelled in the catalog); and
- is used entirely at your own risk — the Maintainers do not control, vet for safety, warrant, or assume responsibility for any Third-Party Tool, its behaviour, its availability, or its effects.

Before you run any Catalogued Tool, you are responsible for verifying its source, integrity, license, and legality where you are, and for understanding what it does before you point it at a Target. Catalog entries (links, descriptions, tags, mappings) are provided for convenience and may be inaccurate or out of date.

## Compliance with Laws, Export Controls & Sanctions

You are **solely responsible** for determining which laws apply to you and your activities, and for complying with them. Depending on where you are, where your Target is, and who is involved, laws and regimes **such as** the following **may** apply — this list is illustrative, **not exhaustive**, and the Maintainers make **no** representation about whether or how any of them applies to you:

- the United States **Computer Fraud and Abuse Act (CFAA)** and related state and federal law;
- the United Kingdom **Computer Misuse Act 1990**;
- the EU **Directive 2013/40/EU** on attacks against information systems and local implementing laws, and other countries' computer-misuse and cybercrime laws;
- **data-protection and privacy** law (for example, the **GDPR**, **UK GDPR**, **CCPA/CPRA**, and local equivalents);
- **export-control and dual-use** regulations (for example, the **Wassenaar Arrangement**, the US **EAR**, and EU **Regulation 2021/821**) and economic **sanctions** programmes (for example, those administered by **OFAC**, the **EU**, **UK OFSI**, or the **UN**); and
- any other criminal, civil, contractual, or regulatory obligations binding on you.

You must not download, use, export, re-export, or make NetGuardian or the Catalogued Tools available to any person, entity, or destination prohibited by applicable export-control or sanctions law. When in doubt, consult qualified legal counsel.

## Responsible & Coordinated Vulnerability Disclosure

If you discover a vulnerability — whether in a Target you are authorized to test, in a Catalogued Tool, or in NetGuardian itself — the Maintainers encourage **responsible, coordinated disclosure**:

- report it **privately** to the affected party (or the tool's maintainers) first, before any public disclosure;
- give a **reasonable, good-faith time** to investigate and remediate;
- access, modify, and retain **no more data than is necessary** to demonstrate the issue, and do no harm; and
- follow any disclosure policy, `security.txt`, VDP, or bug-bounty terms the affected party provides.

To report a security issue **in NetGuardian itself**, contact the Maintainers privately at `[security contact email]` (see `SECURITY.md`, if present) rather than opening a public issue. Finding a vulnerability never authorizes you to exceed your scope or to act against systems you are not permitted to test.

## Relationship to the GPL-3.0 License

NetGuardian's **software and source code** are licensed to you under the **GNU General Public License, version 3.0 (GPL-3.0)** (see the `LICENSE` file). Your rights to **run, study, copy, modify, and distribute** the Software are governed **exclusively** by the GPL-3.0.

- **This document is about conduct, not code.** The Acceptable Use, Authorization, and Prohibited Uses sections are **conduct expectations and a disclaimer** about how you choose to use the Software in the real world — not a software license, not a grant, and not a restriction on the GPL-3.0 grant.
- **No further restrictions.** Nothing in these Terms modifies, revokes, limits, or adds any condition or "further restriction" (within the meaning of the GPL-3.0) to the rights the GPL-3.0 grants you over the Software or its source.
- **GPL-3.0 controls on conflict.** If anything in these Terms is ever read as conflicting with the GPL-3.0 as applied to the Software or its source, **the GPL-3.0 controls** and the conflicting part of these Terms does not apply.

Trademarks, names, and logos of the Project, the Maintainers, and any Third-Party Tool remain the property of their respective owners; no trademark rights are granted by the GPL-3.0 or by these Terms.

## Disclaimer of Warranties

Consistent with **Section 15 of the GPL-3.0**, and to the maximum extent permitted by applicable law:

**THE SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,** including but not limited to the implied warranties of **merchantability, fitness for a particular purpose, title, and non-infringement.** The Maintainers do not warrant that the Software or any catalog data is accurate, complete, current, secure, error-free, or uninterrupted, or that it will meet your requirements. **The entire risk as to the quality, performance, safety, and results of using the Software and any Catalogued Tool is with you.**

## Limitation of Liability

Consistent with **Section 16 of the GPL-3.0**, and to the maximum extent permitted by applicable law:

**In no event will the Maintainers or any contributor be liable to you for any damages** — including any general, special, incidental, consequential, punitive, or exemplary damages; loss of data, profits, goodwill, or business; service interruption; or damage to systems or property — **arising out of or relating to the use or inability to use NetGuardian or any Catalogued Tool, even if advised of the possibility of such damages,** and regardless of the legal theory. This includes any liability for **your** conduct, your Targets, the outcomes of your security testing (authorized or not), and your use or misuse of any Third-Party Tool. Some jurisdictions do not allow certain exclusions or limitations; where that is the case, the above applies to the fullest extent permitted.

## Indemnification

*(Maintainers: this section conditions use and should be confirmed with counsel; some projects omit it.)* To the maximum extent permitted by applicable law, you agree to **indemnify, defend, and hold harmless the Maintainers and contributors** from and against any claims, demands, damages, losses, liabilities, costs, and expenses (including reasonable legal fees) arising out of or related to: (a) your use or misuse of the Software or any Catalogued Tool; (b) your violation of these Terms; (c) your violation of any law, regulation, Authorization, or third-party right; or (d) any action you take against any Target. **Nothing in this section expands any obligation beyond what the GPL-3.0 permits with respect to the Software itself, or imposes any "further restriction" on your GPL-3.0 rights.**

## Contributions

Contributions are welcome — see `CONTRIBUTING.md` for how to add or edit a catalog entry and run the checks. Unless you state otherwise in writing, you agree that any contribution you submit for inclusion in NetGuardian is **licensed under the GPL-3.0** on the same terms as the Project (inbound = outbound), and you confirm you have the right to contribute it. The Maintainers may decline, modify, or revert any contribution at their discretion.

## Changes to These Terms

The Maintainers may update these Terms from time to time. Changes take effect when published to the Project repository, and the **Effective date** above will be updated; material changes will be noted in the repository's history (commits / releases). Your continued use of NetGuardian after changes are published constitutes acceptance of the revised Terms. Because the Software is distributed under the GPL-3.0, any version you already hold remains usable under the GPL-3.0 terms applicable to that version.

## Governing Law

These Terms are intended to be governed by the laws of `[governing jurisdiction]`, without regard to its conflict-of-laws principles — **to be confirmed by the Maintainers with legal counsel.** This choice concerns these conduct Terms and disclaimers only and **does not affect the GPL-3.0** as it applies to the Software and its source.

## Severability

If any provision of these Terms is held invalid, unlawful, or unenforceable, that provision will be modified to the minimum extent necessary to make it enforceable (or, if it cannot be, severed), and the remaining provisions will continue in full force and effect.

## Contact

- **Project:** NetGuardian — `https://github.com/BladeIV/Cybersec-Framework`
- **General / project questions:** `[contact email]` or the repository's issue tracker
- **Security reports (private):** `[security contact email]` (see `SECURITY.md`, if present)
- **Governing jurisdiction (to be completed with counsel):** `[governing jurisdiction]`

See also: `LICENSE` (GPL-3.0), `README.md`, and `CONTRIBUTING.md`.

---

*NetGuardian is maintained by the Maintainers and distributed as free software under the GPL-3.0. These Terms govern conduct and are provided alongside — not in place of — that license. This template is not legal advice.*
