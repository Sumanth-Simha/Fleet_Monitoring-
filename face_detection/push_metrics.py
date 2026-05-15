from supabase_client import supabase
import time

# Controls how frequently DB updates happen
last_push_time = 0


def push_driver_metrics(metrics, driver_state):
    global last_push_time

    current_time = time.time()

    # Update only once every second
    if current_time - last_push_time < 1:
        return

    try:
        response = supabase.table("live_driver_state").update({
            "ear": float(metrics.get("ear", 0)),
            "perclos": float(metrics.get("perclos", 0)),
            "blink_rate": int(metrics.get("blink_rate", 0)),
            "driver_state": str(driver_state),
            "fatigue_score": float(metrics.get("drowsiness_score", 0)),
            "eye_closure_duration": float(
                metrics.get("avg_closure_duration", 0)
            )
        }).eq("id", 1).execute()

        print("[SUPABASE LIVE ROW UPDATED SUCCESSFULLY]")

        last_push_time = current_time

    except Exception as e:
        print(f"[SUPABASE ERROR]: {e}")
