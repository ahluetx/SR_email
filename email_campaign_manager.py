import requests

def get_campaign_details(access_token, campaigns_endpoint, campaign_name):
    """
    Fetches the details of a specific campaign by name.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(campaigns_endpoint, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error getting campaign details: {response.status_code}, {response.text}")

    campaigns = response.json().get('campaigns', [])
    target_campaign = next((c for c in campaigns if c['name'] == campaign_name), None)

    if not target_campaign:
        print(f"Campaign {campaign_name} not found.")
        return None

    return target_campaign

def update_campaign(access_token, update_campaign_endpoint, campaign_data):
    """
    Updates the campaign with the specified data.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.put(update_campaign_endpoint, json=campaign_data, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error updating email campaign activity: {response.status_code}, {response.text}")

    print("Email campaign activity updated successfully with contact list!")

def schedule_campaign(access_token, schedule_campaign_endpoint, schedule_campaign_data):
    """
    Schedules the campaign for sending.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(schedule_campaign_endpoint, json=schedule_campaign_data, headers=headers)

    if response.status_code != 201:
        raise Exception(f"Error scheduling campaign: {response.status_code}, {response.text}")

    print("Campaign scheduled successfully!")
