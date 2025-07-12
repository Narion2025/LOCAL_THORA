import asyncio
from pathlib import Path
import requests
import yaml

from memory.memory_manager import MemoryManager

# When enabled, THOR will ask a follow-up question after each response
FOLLOW_UP_MODE = True

CONFIG_PATH = Path("config/config.yaml")


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def send_phi4(messages, config):
    local_cfg = config.get("llm", {}).get("providers", {}).get("local", {})
    endpoint = local_cfg.get("endpoint", "http://localhost:1234/v1")
    model = local_cfg.get("model", "phi-4-mini-reasoning")
    payload = {
        "model": model,
        "messages": messages,
        "temperature": local_cfg.get("temperature", 0.2),
        "max_tokens": local_cfg.get("max_tokens", 800),
    }
    resp = requests.post(f"{endpoint}/chat/completions", json=payload, headers={"Content-Type": "application/json"})
    if resp.status_code == 200:
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    raise RuntimeError(f"Phi-4 request failed: {resp.status_code}")


def generate_follow_up(history, config):
    """Ask Phi-4 for a short follow-up question"""
    prompt = (
        "Formuliere eine kurze Nachfrage, um den Benutzer besser zu verstehen. "
        "Stelle nur eine Frage."
    )
    follow_messages = history + [{"role": "system", "content": prompt}]
    return send_phi4(follow_messages, config)


def main():
    config = load_config()
    memory = MemoryManager(config)
    system_prompt = (
        "Du bist THOR im Lernmodus. Stelle dem Benutzer proaktiv Fragen, um seine\n"
        "Ziele, Vorlieben und Arbeitsweisen kennenzulernen. Halte die Antworten\n"
        "kurz und fasse Erkenntnisse zusammen."
    )
    messages = [{"role": "system", "content": system_prompt}]
    print("🧠 THOR Lernumgebung gestartet. Tippe 'exit' zum Beenden.")
    while True:
        user_input = input("Du: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        messages.append({"role": "user", "content": user_input})
        try:
            reply = send_phi4(messages, config)
        except Exception as e:
            print(f"Fehler: {e}")
            break
        messages.append({"role": "assistant", "content": reply})
        print(f"THOR: {reply}\n")
        asyncio.run(memory.store_conversation(user_input, reply))

        if FOLLOW_UP_MODE:
            try:
                follow_q = generate_follow_up(messages, config)
                messages.append({"role": "assistant", "content": follow_q})
                print(f"THOR Nachfrage: {follow_q}")
                follow_input = input(
                    "Du (Antwort auf Nachfrage, Enter überspringen): ")
                if follow_input.strip().lower() in {"exit", "quit"}:
                    break
                if follow_input.strip():
                    messages.append({"role": "user", "content": follow_input})
                    follow_reply = send_phi4(messages, config)
                    messages.append({"role": "assistant", "content": follow_reply})
                    print(f"THOR: {follow_reply}\n")
                    asyncio.run(memory.store_conversation(follow_input, follow_reply))
            except Exception as e:
                print(f"Fehler bei Nachfrage: {e}")


if __name__ == "__main__":
    main()
