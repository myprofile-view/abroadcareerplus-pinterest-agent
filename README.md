# AbroadCareerPlus Pinterest Agent v2

This version generates a country-themed vertical pin, can use a photo you provide, and includes an optional Pinterest API publishing workflow.

## What it can do
- Create a 1000x1500 (2:3) Pinterest pin.
- Country color themes for Norway, UK, France, Denmark, Netherlands, Canada, USA, Romania, Brunei, and a default international theme.
- Add a background photo from a direct HTTPS image URL you own or are licensed to use.
- Create title, description, destination link, alt text and hashtags.
- Optionally publish through Pinterest API v5 after you configure API credentials and GitHub Pages.

## A. Update your existing GitHub repository
Upload/replace these files while keeping the folder path:
- `agent.py`
- `publish_pin.py`
- `requirements.txt`
- `.github/workflows/create-pin.yml`
- `README.md`

The workflow must be exactly `.github/workflows/create-pin.yml`, not in the repository root.

## B. Generate a pin first (no Pinterest API required)
1. Open your repository → Actions → **Create and optionally publish Pinterest Pin** → Run workflow.
2. Enter title, country, and the exact article URL.
3. Optional: enter a direct HTTPS URL for an image you own or have a license to use. It must link directly to an image file, not an ordinary web page. Leave blank to use the built-in designed background.
4. Leave **Publish after image generation** unchecked.
5. Run the workflow, download the `pinterest-pin` artifact, and inspect `pin.jpg` and `pin.json`.

## C. Pinterest API setup (required only for auto-publishing)
Pinterest API publishing is not automatic until Pinterest approves your app and you configure valid credentials. Pinterest's current docs require a Pinterest business account, app registration/review, and appropriate scopes. See:
- Connect an app: https://developer.pinterest.com/docs/getting-started/connect-app/
- Authentication: https://developer.pinterest.com/docs/getting-started/set-up-authentication-and-authorization/
- Create Pins: https://developer.pinterest.com/docs/work-with-organic-content-and-users/create-boards-and-pins/

1. Convert/use a Pinterest Business account and verify its email.
2. In Pinterest Developers, connect an app and request trial access. Wait for approval.
3. Obtain an OAuth access token with `pins:write` and the board access scopes required by the API. Keep the token private.
4. Find your target board's ID using the API's board-list endpoint or Pinterest's approved developer tools.
5. In GitHub repository → Settings → Secrets and variables → Actions → New repository secret, add:
   - `PINTEREST_ACCESS_TOKEN` = OAuth access token (must have `pins:write`)
   - `PINTEREST_BOARD_ID` = ID of the destination board
6. Configure GitHub Pages: repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
   - The generated image is temporarily deployed to Pages so Pinterest can fetch its public HTTPS image URL.
   - This publishing workflow makes the generated image available at a public Pages URL. Do not use this feature if you do not want the generated pin image to be publicly accessible.
   - GitHub Pages availability for a private repository depends on your GitHub plan. If unavailable, use a public repository with no secrets in source, or host the image on your own website.
7. Run the workflow with **Publish after image generation** checked. It will build the pin, deploy the image, then call `POST https://api.pinterest.com/v5/pins`.
8. Check the workflow log for a Pinterest Pin ID. If it fails, read the API error; common causes are app not approved, missing `pins:write`, expired/invalid token, wrong board ID, or Pages not enabled.

## Security and review
- Never put Pinterest tokens or app secrets in files or commit them to Git.
- The workflow publishes only when you explicitly check the publish option.
- First test without publishing. Review the generated image and JSON.
- Only use photos you own or have permission to use.
- Verify vacancies; do not invent employer hiring claims, salaries or deadlines.
- Keep publication volume reasonable and avoid repetitive or misleading Pins.
