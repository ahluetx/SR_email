import requests
import datetime

def create_contact_list(access_token, list_endpoint):
    """
    Creates a new contact list with today's date.
    """
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    new_list_name = f"conf_{today_date}"

    list_payload = {
        "name": new_list_name,
        "description": "A list of people signed up for an event in the last 24 hours"
    }

    list_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(list_endpoint, json=list_payload, headers=list_headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error creating list: {response.status_code}, {response.text}")

def delete_previous_day_list(access_token, list_endpoint):
    """
    Deletes the contact list created the previous day.
    """
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    target_list_name = f"conf_{formatted_date}"

    response = requests.get(list_endpoint, headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve contact lists: {response.text}")

    lists = response.json().get("lists", [])
    target_list = next((lst for lst in lists if lst["name"] == target_list_name), None)

    if not target_list:
        print(f"List '{target_list_name}' not found")
        return

    delete_endpoint = f"{list_endpoint}/{target_list['list_id']}"
    delete_response = requests.delete(delete_endpoint, headers={"Authorization": f"Bearer {access_token}"})

    if delete_response.status_code == 202:
        print(f"Successfully deleted list '{target_list_name}'")
    else:
        raise Exception(f"Failed to delete list '{target_list_name}': {delete_response.text}")

def upload_contacts(access_token, list_id, csv_contents, upload_endpoint):
    """
    Uploads contacts to the specified list using the provided CSV contents.
    """
    list_ids = [list_id]

    upload_data = {
        "file": ("contacts.csv", csv_contents.encode('utf-8'), "text/csv"),
        "list_ids": (None, ",".join(list_ids))
    }

    upload_headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(upload_endpoint, files=upload_data, headers=upload_headers)
    if response.status_code == 201:
        print("Contacts uploaded successfully!")
    else:
        raise Exception(f"Error uploading contacts: {response.status_code}, {response.text}")