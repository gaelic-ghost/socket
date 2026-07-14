# Web And API Test Plan

Record:

- WSTG/API test identifier or named security property;
- exact endpoint, method, content type, schema, and environment;
- account, role, tenant, and resource owner;
- normal baseline request/response;
- one changed input or state;
- expected security behavior;
- observed response, server-side evidence, and side effect;
- negative control and cleanup;
- rate/concurrency and stop condition.

Use the current [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) and [ZAP documentation](https://www.zaproxy.org/docs/). Review Nuclei templates before use; a template match is a validation candidate, not a confirmed finding.
