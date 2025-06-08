import json

def get_sesion(redis_client, candidato_id: str):
    session_data = redis_client.get(f"session:{candidato_id}")
    return json.loads(session_data) if session_data else None

def get_all_sesiones(redis_client):
    sesiones = []
    for key in redis_client.scan_iter("session:*"):
        session_data = redis_client.get(key)
        if session_data:
            sesiones.append({
                "candidato_id": key.split(":")[1],
                **json.loads(session_data)
            })
    return sesiones

def delete_sesion(redis_client, candidato_id: str):
    return redis_client.delete(f"session:{candidato_id}")

def add_action(redis_client, candidato_id: str, action_name: str):
    key = f"session:{candidato_id}"
    session_data_str = redis_client.get(key)
    if not session_data_str:
        return None
    session_data = json.loads(session_data_str)
    session_data.setdefault("recent_actions", []).append(action_name)
    redis_client.set(key, json.dumps(session_data))
    return session_data

def crear_sesion(redis_client, candidato_id: str):
    key = f"session:{candidato_id}"
    if redis_client.exists(key):
        return False 

    initial_data = {
        "candidato_id": candidato_id,
        "recent_actions": []
    }
    redis_client.set(key, json.dumps(initial_data))
    return True
