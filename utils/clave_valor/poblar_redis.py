import redis
import json
import sys
import random
from datetime import datetime, timedelta
from decouple import config
from pymongo import MongoClient

def get_mongo_db():
    """Establishes connection to MongoDB and returns the database object."""
    mongo_uri = config("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client["talentum_demo"]

def generate_random_session(candidate_id):
    """Generates a plausible random session object for a candidate."""
    now = datetime.utcnow()
    status = random.choice(["active", "inactive", "expired"])
    last_login = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
    login_attempts = random.randint(1, 5) if status != "active" else 1
    
    possible_actions = ["view_profile", "search_jobs", "apply_job", "update_cv", "view_course", "logout"]
    recent_actions = random.sample(possible_actions, k=random.randint(0, 4)) if status == "active" else []

    return {
        "status": status,
        "last_login": last_login.isoformat() + "Z",
        "login_attempts": login_attempts,
        "recent_actions": recent_actions,
        "generated_at": now.isoformat() + "Z"
    }

def populate_redis():
    """
    Connects to Redis & MongoDB, clears Redis, and populates it with dynamically generated session data
    based on candidates from MongoDB.
    """
    log = {
        "status": "in_progress",
        "actions": []
    }

    try:
        # --- 1. Connect to Redis ---
        redis_url = config("REDIS_URL", default="redis://localhost:6379")
        r = redis.from_url(redis_url, decode_responses=True)
        log["actions"].append({"action": "Connecting to Redis", "details": f"URL: {redis_url}", "status": "success"})

        # --- 2. Connect to MongoDB ---
        db = get_mongo_db()
        log["actions"].append({"action": "Connecting to MongoDB", "status": "success"})

        # --- 3. Fetch candidate IDs from MongoDB ---
        candidatos = list(db.candidatos.find({}, {"_id": 0, "id": 1}))
        candidate_ids = [c["id"] for c in candidatos]
        if not candidate_ids:
            raise Exception("No candidates found in MongoDB. Please populate MongoDB first.")
        log["actions"].append({"action": "Fetching candidates from MongoDB", "details": f"Found {len(candidate_ids)} candidates.", "status": "success"})

        # --- 4. Clear existing data in Redis ---
        r.flushdb()
        log["actions"].append({"action": "Clearing Redis database (FLUSHDB)", "status": "success"})

        # --- 5. Populate Redis with new, dynamic data ---
        # To avoid creating too many sessions, let's create for a sample of candidates
        # We'll ensure our main test candidate 'cand_001' is always included.
        guaranteed_ids = {'cand_001'}
        
        # Make sure guaranteed IDs exist in the main list
        valid_guaranteed_ids = [cid for cid in guaranteed_ids if cid in candidate_ids]
        
        remaining_ids = [cid for cid in candidate_ids if cid not in guaranteed_ids]
        
        sample_size = min(len(remaining_ids), 14) # 14 + our 1 guaranteed ID
        
        selected_ids = valid_guaranteed_ids + random.sample(remaining_ids, sample_size)

        sessions_created_count = 0
        for cid in selected_ids:
            session_key = f"session:{cid}"
            session_data = generate_random_session(cid)
            r.set(session_key, json.dumps(session_data))
            log["actions"].append({"action": "Creating session", "details": f"Key: {session_key}", "status": "success"})
            sessions_created_count += 1

        log["status"] = "success"
        log["summary"] = f"Successfully created {sessions_created_count} dynamic session keys based on MongoDB candidates."

    except redis.exceptions.ConnectionError as e:
        log["status"] = "error"
        log["summary"] = "Failed to connect to Redis."
        log["error_details"] = str(e)
        log["actions"].append({"action": "Connecting to Redis", "status": "failed", "error": str(e)})
    except Exception as e:
        log["status"] = "error"
        log["summary"] = "An unexpected error occurred."
        log["error_details"] = str(e)
    finally:
        # Print the final log as a JSON string to stdout
        print(json.dumps(log, indent=2))
        if log["status"] == "error":
            sys.exit(1)

if __name__ == "__main__":
    populate_redis()