# Contributing to Hanceville Entertainment and Shopping

Charles Adams is the only approver for this website. Nothing publishes without his approval of a named package.

## How work flows

1. Every change starts as an Issue using one of the issue forms in `.github/ISSUE_TEMPLATE`.
2. Work happens on a branch. Changes land through a pull request, never by pushing directly to `main`.
3. Open the pull request as a Draft while work is in progress, then mark it Ready for review when it is verified.
4. Link the issue with a closing keyword, for example `Closes #12`.
5. The Lighthouse CI gate must pass. Scores are reported as measured, never as guaranteed.

## Standards

- Raw hand written code: plain HTML, CSS, and JavaScript. No frameworks and no build pipeline.
- Every listing fact carries its recorded source. A fact with no source is researched or held, never published, and no detail is ever invented or copied from another listing.
- A change is verified by rendering and exercising the page at phone, tablet, and computer widths, not by file comparison alone.
- Security and accuracy scans run before and after every update.
- Any borrowed code or pattern must have its source and licence recorded before merge.

The full GitHub working standard lives in the private Control Center repository, in `docs/GITHUB_STANDARD.md`.
