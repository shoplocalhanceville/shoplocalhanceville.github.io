# GitHub Codespaces and prebuilds

This repository is a static GitHub Pages site. Its tracked source is primarily HTML, CSS, JavaScript, JSON, and Python tooling. The repository README mentions a `../build.py` script, which is outside this repository; it is not included in this Codespaces environment. You can edit and validate tracked files here, but any workflow that depends on that external script must be run in the environment where the script is available.

## Dev container

`.devcontainer/devcontainer.json` provides Python 3.12 and Node.js 20. It does not install site dependencies or run a site build, because no in-repository package manifest or build entry point was identified. On creation it reports the installed runtime versions. This makes the environment small and avoids silently running a generator that is not present in the repository.

Useful checks from the repository root:

```sh
python3 tools/seo_head.py --check
python3 tools/audit.py
node --check app.js
```

The audit is read-only unless its own help or documentation says otherwise. Review a command's behavior before running it. Run `python3 tools/seo_head.py` without `--check` only when intentionally applying its SEO edits.

## Configure a Codespaces prebuild

Prebuild configuration is a GitHub repository setting, not a file that can be enabled by committing code. A repository administrator can configure it in **Settings → Codespaces → Prebuilds**:

1. Choose **Set up prebuild** and select the branch or branches collaborators commonly use (start with `main`).
2. Select the dev container configuration at `.devcontainer/devcontainer.json`.
3. Choose the regions and machine type appropriate for the team, then review the displayed storage and compute implications.
4. Choose the update trigger and cadence that suit the change rate of the branch. Prebuilds can be updated when relevant commits are pushed; review GitHub's current UI and documentation for the available trigger choices.
5. Save the configuration and confirm that the first prebuild workflow completes successfully in the repository's Actions tab.
6. Create a test Codespace from the configured branch and verify that Python and Node are available and the intended project checks work.

Prebuilds prepare an environment snapshot for faster Codespace creation; they do not publish the static site or replace GitHub Pages deployment. They may consume Actions usage and Codespaces storage/compute. Check current account/org plan, billing, spending limits, and repository policy in GitHub Settings before enabling them. GitHub-hosted prebuild settings, regions, machine options, eligibility, and billing are controlled by GitHub and cannot be guaranteed or activated by repository code alone.

## Maintenance

Keep the dev container aligned with actual in-repository tooling. If a checked-in package manifest, dependencies, or build command is added later, document and install only what is required, then verify the setup both in a normal Codespace and in a newly generated prebuild. Avoid putting credentials or secrets in the image or prebuild build steps; use Codespaces secrets for sensitive values and do not expose secrets to untrusted pull request code.

## Official references

- [About GitHub Codespaces prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds)
- [Configuring prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/configuring-prebuilds)
- [Managing prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/managing-prebuilds)
- [Adding a dev container configuration](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-project-for-codespaces)
