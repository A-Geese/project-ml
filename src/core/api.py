import requests
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/get_mpp_from_postal/{postal}")
async def get_mpp_from_postal(postal: str):
    url = f"https://www.ola.org/en/views/ajax?_wrapper_format=drupal_ajax&field_full_name_by_first_name_value=&field_member_id_value={postal}&field_party_target_id=All&view_name=current_members&view_display_id=current_members_grid&view_args=&view_path=%2Fnode%2F96456&view_base_path=&view_dom_id=3a6999bf2b67341fa644a4cd4494792b7de5daacb5a250e1f6d543d17c15a1ca&pager_element=0&_drupal_ajax=1&ajax_page_state%5Btheme%5D=de_theme&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=eJyFkF1uAyEMhC-E4CnnQQacjSuwVwybdnP6rkLaVFWkvFgzn_9kUynDSPdAD-HP3XS4VOm2hyTm6YO-XL4YWEPp20rVT_eAsUoKU_oMuFwJOFoJ_KMbA7Twb06tHDnrfKjeqMqNXeE4Ltx4Nj6d2cDotJ6eDGiuksW89c46YuOWuCO8YPHYxwP38iJoAkiqHBOpcg-vseuM1RRy5WOObuGf99n0LMvbMoy9ii4OOwa3edhV-BPhHudn_4JmZav8DcoTnlE"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,en-CA;q=0.8",
        "cookie": "_gid=GA1.2.563051065.1732390621; _ga=GA1.2.1756671859.1732390620; _gat_gtag_UA_2412076_15=1; _gat_UA-2412076-15=1; _ga_ZRFV1YLS89=GS1.1.1732430514.6.1.1732431864.0.0.0",
        "priority": "u=1, i",
        "referer": "https://www.ola.org/en/members/current",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }

    response = requests.get(url, headers=headers)
    res = response.json()
    for command in res:
        if command.get("command") == "insert" and command.get("data"):
            html_content = command["data"]
            soup = BeautifulSoup(html_content, "html.parser")
            name_element = soup.find("h3")
            if name_element:
                name = name_element.get_text(strip=True)
                return {"message": name}
    raise HTTPException(status_code=400, detail="Invalid postal code format.")


@app.post("/summarize_policy")
async def summarize_policy(url: str):
    try:
        response = requests.post(url)
        response.raise_for_status()
        return {"status": "success", "content": response.text}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}