from datetime import datetime

def log_to_file(filename: str, content: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_entry = f"[{timestamp}]\n{content}\n{'=' * 50}\n"
    with open(filename, "a") as f:
        f.write(full_entry)
