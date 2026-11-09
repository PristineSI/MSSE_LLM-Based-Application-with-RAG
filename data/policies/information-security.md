# Information Security and Acceptable Use Policy

> **Synthetic academic exercise:** Fictional policy text created solely for the Northstar Labs RAG project. Northstar Labs does not exist. This is not cybersecurity, legal, or professional advice.

**Policy ID:** NL-SEC-004 | **Version:** 1.0 (fictional) | **Effective:** 1 January 2025 (fictional) | **Owner:** Information Security (fictional)

## 1. Purpose, scope, and information classes

This policy establishes basic safeguards for fictional Northstar Labs information, accounts, and devices. It applies to employees, temporary workers, and contractors who receive company access. A manager sponsoring a contractor is responsible for confirming that the contractor receives this policy before access is granted. These rules are written for a classroom scenario and do not describe a real security program.

**Public** information is approved for public release. **Internal** information is intended for company use but is not highly sensitive. **Confidential** information includes nonpublic business plans, customer records, or employee details. **Restricted** information includes credentials, security keys, sensitive personal data, and data whose exposure could create serious harm. If classification is unclear, treat it as Confidential and ask Information Security.

Users should access only the information needed for their assigned work. They should use approved company systems, keep records in authorized locations, and follow project-specific handling instructions. Restricted information must never be pasted into a public AI tool, personal email, personal cloud drive, or public code repository.

Security controls are not optional because a task is urgent. If an approved tool is unavailable, contact the Help Desk for an approved alternative rather than bypassing encryption, multifactor authentication, or access controls.

## 2. Accounts, passwords, and authentication

Every user must have an individual account. Sharing passwords or authentication codes is prohibited, including with a manager or Help Desk employee. Users must enable multifactor authentication on every company account that supports it. The preferred method is an approved authenticator application or hardware security key. SMS may be used only when Information Security approves it as the available fallback.

Passwords should be unique to Northstar Labs and at least 14 characters long when the service permits. An approved password manager may be used to create and store them. Users should not reuse a company password on a personal site, write it on a visible note, send it in chat, or place it in source code. Passwords must be changed promptly if compromise is suspected; routine changes are not required unless the service or Information Security directs them.

Users must lock their screen when stepping away and sign out of shared workstations after use. They should review login prompts before approving them. An unexpected multifactor prompt must be denied and reported to the Help Desk immediately. Recovery codes should be stored in an approved secure location, not in email or an unencrypted personal note.

Managers may request access changes through the access-request process, but may not ask an employee to disclose a password. Access should be removed when a role changes or a person leaves. The system owner reviews privileged access at least once every quarter.

## 3. Devices, software, and network use

Company work must be performed on a company-managed device unless Information Security gives written approval for a specific alternative. Users must keep operating-system updates and company security software enabled. They must not disable endpoint protection, encryption, screen lock, or device-management controls. Lost, stolen, or damaged devices must be reported as described in Section 5.

Software may be installed only from the company catalog or after approval from the Help Desk or Information Security. Browser extensions, command-line tools, and AI coding tools count as software for this rule. Users should not connect unknown USB storage or personal peripherals that can read company data. Personal use of a company device must remain incidental and must not interfere with work or weaken safeguards.

When working remotely, users should use a trusted private network protected with a strong router password. Public Wi-Fi may be used only with the company-approved secure connection. Users should not discuss Confidential or Restricted information where others can overhear or leave a screen visible to the public. The remote-work policy defines the approved worksite; this policy defines the security controls used there.

Company data must be stored in approved company services. Local copies should be minimized and deleted when no longer needed. Removable media, personal cloud accounts, personal messaging, and personal email are not approved storage or transfer methods for Confidential or Restricted data.

## 4. Data handling and AI tools

Before sharing data, users must confirm the recipient, purpose, classification, and authorization. External sharing of Confidential information requires approval from the data owner. Restricted information may be shared externally only through a method specifically approved by Information Security and the data owner. Public information may be shared only if the owner has approved publication.

Users may use an AI tool for public or synthetic information when the tool is approved for the task. Confidential or Restricted information must not be entered into a consumer AI service. AI-generated code, summaries, or recommendations must be reviewed by a person before use. Users must not ask an AI tool to make a final employment, access, financial, legal, or safety decision about a person.

For this academic repository, only fictional policy documents, synthetic questions, and non-sensitive code examples should be committed. API keys belong in a local environment file excluded by `.gitignore` or in an approved secret store. The `.env.example` file may show variable names but must contain placeholder values only. If a real secret is accidentally committed, revoke or rotate it immediately and notify Information Security; deleting the file alone does not invalidate the exposed secret.

Printed Confidential material should be collected promptly and stored in a locked area. Users should dispose of it through approved shredding. Screenshots and recordings must not expose secrets, personal information, or unrelated private content.

## 5. Security incidents and response

A security incident includes a lost device, suspected account takeover, unexpected authentication prompt, malware warning, accidental disclosure, misdirected email, suspicious link, exposed credential, or unusual access to company information. Users should report a suspected incident to the Help Desk and Information Security within one hour of discovery, using the approved incident channel. If that channel is unavailable, contact the Help Desk by phone and follow up in writing.

A report should include what happened, when it was noticed, the account or device involved, what information may be affected, and steps already taken. Users should not speculate about blame, delete relevant evidence, investigate beyond their role, or contact an outside party on the company's behalf. If a device is missing, provide the last known location and whether it was locked or connected.

Information Security coordinates containment, investigation, recovery, and communications. It may suspend an account or disconnect a device to reduce risk. Users should preserve messages, filenames, and timestamps when safe. The incident lead determines whether affected teams or customers need notice through an approved channel.

Employees who report an incident in good faith should be treated respectfully. A mistaken click or accidental disclosure should be reported promptly; concealing it can make the impact worse. Managers should help the reporting employee contact the response team and should not promise that no consequences will follow before the facts are reviewed.

## 6. Roles, monitoring, exceptions, and review

Users are responsible for following safeguards and reporting suspicious activity. Managers approve access based on work need and review it when duties change. System owners configure controls and keep services current. The Help Desk supports managed devices and account recovery. Information Security owns this policy, reviews incidents, and approves security exceptions.

Company systems may create access and security logs for service reliability, fraud prevention, and incident response. Access to these logs is limited to authorized personnel. Users should not assume company systems are private personal storage. This fictional statement does not describe monitoring by any real employer.

An exception request must identify the control, business need, duration, affected data or system, alternative safeguards, and responsible manager. Information Security must approve the exception in writing before the control is bypassed. Exceptions expire on the written end date and must be renewed if still needed. No exception may authorize sharing passwords or knowingly publishing Restricted data.

Information Security reviews this policy each January and after a significant incident. The current version and incident contact details should be kept in the repository documentation. Any answer generated by the RAG application must cite the relevant section and direct immediate incidents to the fictional Help Desk process instead of improvising new instructions.
