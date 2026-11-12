"""Local Gemma 4 client (Ollama native API). Every call is logged and counted."""
import base64, json, os, time, urllib.request
from pathlib import Path

OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("DG_MODEL", "gemma4:26b")
THINK = os.environ.get("DG_THINK", "0") == "1"
TEMP = float(os.environ.get("DG_TEMP", "0.3"))
SEED = int(os.environ.get("DG_SEED", "0"))


class BudgetExceeded(Exception):
    pass


class LLM:
    """One instance per (problem, level) run. Enforces the call cap and logs to JSONL."""

    def __init__(self, log_path: Path, cap: int | None = None):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.cap = cap
        self.calls = 0
        self.tokens_in = 0
        self.tokens_out = 0
        self.seconds = 0.0

    def remaining(self):
        return None if self.cap is None else self.cap - self.calls

    def __call__(self, role: str, system: str, user: str = "", images: list[Path] | None = None,
                 max_tokens: int = 4096, messages: list[dict] | None = None, step: int | None = None) -> str:
        """One chat completion. Either a single `user` message or a full multi-turn `messages` list (agent loops)."""
        if self.cap is not None and self.calls >= self.cap:
            raise BudgetExceeded(role)
        if messages is None:
            msg = {"role": "user", "content": user}
            if images:
                msg["images"] = [base64.b64encode(Path(p).read_bytes()).decode() for p in images]
            messages = [msg]
        body = {
            "model": MODEL, "stream": False, "think": THINK,
            "messages": [{"role": "system", "content": system}] + messages,
            "options": {"temperature": TEMP, "seed": SEED + self.calls, "num_ctx": 24576,
                        "num_predict": max_tokens},
        }
        t0 = time.time()
        for attempt in range(3):
            try:
                req = urllib.request.Request(f"{OLLAMA}/api/chat", data=json.dumps(body).encode(),
                                             headers={"Content-Type": "application/json"})
                r = json.load(urllib.request.urlopen(req, timeout=1800))
                break
            except Exception as e:  # transient server errors
                if attempt == 2:
                    raise
                time.sleep(5)
        dt = time.time() - t0
        out = r["message"]["content"]
        self.calls += 1
        self.tokens_in += r.get("prompt_eval_count", 0)
        self.tokens_out += r.get("eval_count", 0)
        self.seconds += dt
        with self.log_path.open("a") as f:
            f.write(json.dumps({
                "i": self.calls, "role": role, "step": step, "t": round(dt, 1),
                "tok_in": r.get("prompt_eval_count", 0), "tok_out": r.get("eval_count", 0),
                "n_images": sum(len(m.get("images", [])) for m in messages), "system": system,
                "user": messages[-1]["content"] if len(messages) == 1 else [m["content"] for m in messages], "output": out,
            }) + "\n")
        return out

    def stats(self):
        return {"calls": self.calls, "tokens_in": self.tokens_in, "tokens_out": self.tokens_out,
                "seconds": round(self.seconds, 1)}


def extract_code(text: str, lenient: bool = False) -> str:
    """Return the last ```python block (or the whole text if none). lenient=True (L5 only) also accepts an unclosed block,
    e.g. an answer cut off at the token limit; L0-L4 keep the original behaviour."""
    import re
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, flags=re.S)
    if blocks:
        return blocks[-1].strip()
    if lenient:
        m = re.search(r"```(?:python|py)?\s*\n(.*)$", text, flags=re.S)
        if m:
            return m.group(1).strip()
    return text.strip()


def extract_json(text: str):
    import re
    m = re.findall(r"```(?:json)?\s*\n(.*?)```", text, flags=re.S)
    cands = m + [text]
    for c in cands:
        c = c.strip()
        i, j = c.find("{"), c.rfind("}")
        if i >= 0 and j > i:
            try:
                return json.loads(c[i:j + 1])
            except Exception:
                continue
    return None
