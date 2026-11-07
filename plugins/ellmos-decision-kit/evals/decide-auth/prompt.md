---
max_turns: 6
allowed_tools: [Read, Skill]
---

Our four-person team builds a B2B web app for clinics in Germany. Before launch we must pick the authentication
approach: (a) build our own on top of our web framework, (b) Auth0, or (c) self-hosted Keycloak. Constraints: the app
handles patient-adjacent data, GDPR compliance and EU hosting are required, we have little operations capacity, the
budget is about 300 EUR per month, and enterprise customers will ask for single sign-on later. Decide.
