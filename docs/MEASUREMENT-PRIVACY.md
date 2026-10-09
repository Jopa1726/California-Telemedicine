# Measurement & privacy

## What we measure (useful outcomes)
- California service visits (sessions on `/california/*`).
- Booking **starts** and **completed** bookings (event from the scheduling vendor, not PHI).
- Contact requests (notify + inquiry form submissions, counts only).
- Physician inquiries (recruitment form submissions, counts only).
- Conversion by device (mobile vs. desktop).
- Search performance by state (segment Search Console by path).

## Hard privacy rules (non-negotiable)
- **Never** send to analytics or advertising platforms: diagnoses, any form answers,
  uploaded documents, patient identifiers, or sensitive URL parameters.
- **No advertising pixels** anywhere on the clinical journey.
- **No session replay** in clinical intake or any patient-portal flow.
- Clinical intake/portal pages load **zero** marketing/analytics tags.
- **Marketing email/SMS consent is separate** from clinical consent (enforced in form copy).
- Strip query strings before sending any pageview; never put identifiers in URLs.

## How the build supports this
- Preview ships with **no** third-party scripts, trackers, or pixels (see `head.html` comment).
- `integrations.analytics.enabled` is `false`; enabling it is a deliberate, documented step.
- When enabled: add a single privacy-respecting analytics tag **only** on marketing pages
  (`/california/` content, careers), configured to anonymize IPs and drop query strings;
  exclude the scheduling vendor's intake domain entirely.

## Data minimization & governance
- Public forms collect the minimum (name, email, + state/message or license fields).
- CV uploads disabled until secure storage + access controls exist.
- Document retention periods, access controls, and a vendor configuration list.
- **Do not** describe the service as "HIPAA compliant" based on HTTPS or site design alone —
  only with a documented, BAA-backed vendor configuration reviewed by qualified counsel.
