from supabase_client import supabase

response = supabase.table("driver_metrics").insert({
    "ear": 0.26,
    "perclos": 0.38,
    "blink_rate": 14,
    "driver_state": "Normal"
}).execute()

print(response)
