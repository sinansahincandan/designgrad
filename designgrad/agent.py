"""A persistent coding agent: write code -> run it -> read the result -> fix -> ... until the goal is met.

This is the ReAct-style loop that single-shot TextGrad roles lacked. It is generic: the caller supplies
  run_fn(code)   -> result dict (execution of the artifact)
  feedback_fn(result) -> None when the goal is met, else a text describing what is still wrong
The conversation is multi-turn: every run result is appended as a user turn, so the model sees its own
previous code and the exact error. Every step is one LLM call, logged with role and step index.
"""
from .llm import LLM, BudgetExceeded, extract_code

STEP_USER = """{feedback}

Fix the code. Answer with the complete corrected code in one ```python block (no explanations needed)."""


def solve(llm: LLM, role: str, system: str, task: str, run_fn, feedback_fn, max_steps: int = 4,
          max_tokens: int = 6000, initial_code: str | None = None, lenient: bool = False):
    """Returns dict(code, result, steps, exhausted, history).

    If `initial_code` is given, it is treated as the agent's first attempt (already written by an earlier
    stage, e.g. a TextGrad update) and is run first; the agent only intervenes when it fails."""
    messages = [{"role": "user", "content": task}]
    history = []
    code = initial_code
    step = 0
    if code is None:
        txt = llm(role, system, messages=messages, max_tokens=max_tokens, step=0)
        messages.append({"role": "assistant", "content": txt})
        code = extract_code(txt, lenient)
        step = 1
    else:
        messages.append({"role": "assistant", "content": f"```python\n{code}\n```"})
    result = run_fn(code)
    fb = feedback_fn(result)
    history.append({"step": step, "ok": fb is None, "feedback": (fb or "")[:600]})
    while fb is not None and step < max_steps:
        if sum(len(x["content"]) for x in messages) > 60000:   # only near the context limit (~15k tokens): keep task + latest attempt
            messages = [messages[0], {"role": "assistant", "content": f"```python\n{code}\n```"}]
        try:
            txt = llm(role, system, messages=messages + [{"role": "user", "content": STEP_USER.format(feedback=fb)}],
                      max_tokens=max_tokens, step=step)
        except BudgetExceeded:
            break
        messages.append({"role": "user", "content": STEP_USER.format(feedback=fb)})
        messages.append({"role": "assistant", "content": txt})
        new_code = extract_code(txt, lenient)
        unchanged = new_code.strip() == code.strip()
        code = new_code
        step += 1
        result = run_fn(code)
        fb = feedback_fn(result)
        if fb is not None and unchanged:
            fb = "Your last answer repeated the previous code unchanged; it still fails.\n" + fb
        history.append({"step": step, "ok": fb is None, "feedback": (fb or "")[:600]})
    return {"code": code, "result": result, "steps": step, "exhausted": fb is not None, "history": history}
