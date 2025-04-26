from services.supabase.supabase_client import supabase_post, supabase_get, supabase_delete

SUPABASE_TABLE_REMINDERS = "reminders"

def add_reminder(sender_id: int, message: str, remind_at: str = None, target_id: int = None):
    payload = {
        "message": message,
        "sender_id": sender_id,
        "target_id": target_id if target_id else sender_id,
        "delivered": False
    }
    if remind_at:
        payload["remind_at"] = remind_at
    response = supabase_post(SUPABASE_TABLE_REMINDERS, payload)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    return response.status_code == 201

def list_reminders(sender_id: int):
    params = {
        "sender_id": f"eq.{sender_id}",
        "delivered": "eq.false"
    }
    response = supabase_get(SUPABASE_TABLE_REMINDERS, params)
    if response.status_code == 200:
        return response.json()
    return []

def delete_reminder(reminder_uuid: str):
    filter_query = f"id=eq.{reminder_uuid}"
    response = supabase_delete(SUPABASE_TABLE_REMINDERS, filter_query)
    return response.status_code == 204
