# AbroadCareerPlus Pinterest Pin Agent (Beginner Version)

Create a branded 1000x1500 Pinterest pin image plus SEO metadata. No API key and no paid service required for this first version.

## What it does
- Generates a vertical 2:3 PNG pin
- Creates a JSON file with title, description, destination URL, suggested board, hashtags and alt text
- Runs from GitHub Actions with editable inputs
- Does not publish to Pinterest automatically yet

## GitHub setup
1. Create a repository named `abroadcareerplus-pinterest-agent`.
2. Upload `agent.py`, `requirements.txt`, and `README.md` to the root.
3. Upload `.github/workflows/create-pin.yml` preserving its folders.
4. Open the **Actions** tab and enable workflows if prompted.
5. Select **Create Pinterest Pin** → **Run workflow**.
6. Enter a title, country/region and the exact article URL.
7. Click **Run workflow**.
8. When it finishes, open the run and download the `pinterest-pin` artifact.
9. Extract it. The PNG is the image; the JSON contains Pinterest metadata.

## Run locally (optional)
```bash
pip install -r requirements.txt
python agent.py --title "Norway Offshore Jobs" --country "Norway" --url "https://abroadcareerplus.com/jobs/" --output output
```

## Automatic publishing (later)
Publishing is intentionally not enabled in this beginner version. For automatic creation, an app needs authorized access to Pinterest's official API and a supported business account/permissions. API availability, review requirements and endpoint rules can change. Do not store passwords or tokens in source code. Add credentials only as GitHub Actions secrets after reviewing Pinterest's current developer documentation.

## Best practice
- Use the exact relevant article URL instead of the homepage where possible.
- Check all job details and don't imply an unverified vacancy is confirmed.
- Use only original or properly licensed photos and graphics.
- Review image layout and text before posting.
