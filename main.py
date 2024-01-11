#contact lists must be named conf_YYYY-MM-DD
# "pip install requests time datetime tkinter csv io" to install dependencies
#This program is designed to access Constant Contact using the OAuth2 devise flow, 
#upload a list of contacts from a file stored locally, send an email campaign to the 
#specified list of contacts then delete the list that was used yesterday to avoid 
#causing errors in todays send
import auth
import contact_list_manager
import file_handler
import email_campaign_manager
import datetime

# Global Variables and Constants
scope = "contact_data campaign_data offline_access account_read account_update"
auth_endpoint = "https://authz.constantcontact.com/oauth2/default/v1/device/authorize"
token_endpoint = "https://authz.constantcontact.com/oauth2/default/v1/token"
list_endpoint = "https://api.cc.email/v3/contact_lists"
campaigns_endpoint = "https://api.cc.email/v3/emails"
grant_type = "urn:ietf:params:oauth:grant-type:device_code"
client_id = ""
campaign_name = ""
from_name= ""
from_email = ""
reply_to_email = ""
subject = ""

try:
    # Start OAuth2 Authentication Flow
    auth_response = auth.request_authorization(client_id, auth_endpoint, scope)
    device_code = auth_response["device_code"]
    user_code = auth_response["user_code"]
    verification_uri = auth_response["verification_uri_complete"]
    print("Please visit:", verification_uri)
    print("Enter code:", user_code)

    # Poll for Token
    token_data = auth.poll_for_token(client_id, device_code, token_endpoint, grant_type)
    access_token = token_data["access_token"]

    # Create a New List with Today's Date
    list_response = contact_list_manager.create_contact_list(access_token, list_endpoint)
    list_id = list_response["list_id"]

    # File Handling - Select and Process File
    file_path = file_handler.select_file()
    csv_contents = file_handler.process_file(file_path)

   # Upload Contacts to the List
    upload_endpoint = "https://api.cc.email/v3/activities/contacts_file_import"
    contact_list_manager.upload_contacts(access_token, list_id, csv_contents, upload_endpoint)


    # Get Campaign Details
    campaign = email_campaign_manager.get_campaign_details(access_token, campaigns_endpoint, campaign_name)
    campaign_id = campaign['campaign_id']

    # Update Campaign
    update_campaign_endpoint = f"https://api.cc.email/v3/emails/activities/{campaign_id}"
    campaign_data = {
        "contact_list_ids": [list_id],
        "from_name": from_name,
        "from_email": from_email,
        "reply_to_email": reply_to_email,
        "subject": subject
    }
    email_campaign_manager.update_campaign(access_token, update_campaign_endpoint, campaign_data)

    # Schedule the Campaign
    schedule_campaign_endpoint = f"https://api.cc.email/v3/emails/activities/{campaign_id}/schedules"
    scheduled_date = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(microsecond=0).isoformat() + ".000Z"
    schedule_campaign_data = {"scheduled_date": scheduled_date}
    email_campaign_manager.schedule_campaign(access_token, schedule_campaign_endpoint, schedule_campaign_data)

    # Delete Previous Day's List
    contact_list_manager.delete_previous_day_list(access_token, list_endpoint)

except Exception as e:
    print(f"An error occurred: {e}")


