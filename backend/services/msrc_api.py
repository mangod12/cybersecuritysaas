import httpx

MSRC_API_BASE = "https://api.msrc.microsoft.com/cvrf/v3.0"

async def fetch_msrc_updates():
    url = f"{MSRC_API_BASE}/updates"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"Accept": "application/json"})
        resp.raise_for_status()
        return resp.json().get("value", [])

async def fetch_msrc_update_details(update_id):
    url = f"{MSRC_API_BASE}/cvrf/{update_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"Accept": "application/json"})
        resp.raise_for_status()
        return resp.json()
