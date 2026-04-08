import asyncio
import os
from typing import List, Optional
from openai import OpenAI

from content_moderation.client import ContentModerationEnv
from content_moderation.models import ContentModerationAction

# ENV CONFIG
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "meta-llama/Meta-Llama-3-8b-Instruct"

# PROMPT
SYSTEM_PROMPT = """
You are a content moderation system.

You will receive:
- content
- context
- intent

Decide ONE:
allow / remove / review

Rules:
- Threats or abuse → remove
- Uncertain / sarcastic / harsh → review
- Safe / positive → allow

Reply ONLY with one word:
allow OR remove OR review
"""

# LOGGING (STRICT FORMAT)
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )

# LLM DECISION
def get_decision(client: OpenAI, content, context, intent):
    prompt = f"""
Content: {content}
Context: {context}
Intent: {intent}

Decision:
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=5,
        )

        text = (completion.choices[0].message.content or "").strip().lower()

        # ensure valid output
        if text not in ["allow", "remove", "review"]:
            return "review"

        return text

    except Exception as e:
        print(f"[DEBUG] LLM error: {e}", flush=True)
        return "review"


# MAIN
async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = ContentModerationEnv(base_url="http://localhost:8000")

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task="content_moderation", env="content_moderation", model=MODEL_NAME)

    try:
        # RESET ENV
        result = await env.reset()
        obs = result.observation

        # GET DECISION
        decision = get_decision(client, obs.content, obs.context, obs.intent)

        # STEP ENV (ONLY ONCE)
        result = await env.step(ContentModerationAction(decision=decision))

        reward = result.reward or 0.0
        done = result.done

        rewards.append(reward)
        steps_taken = 1

        log_step(step=1, action=decision, reward=reward, done=done, error=None)

        # SCORE
        score = reward
        success = score >= 0.5

    finally:
        try:
            await env.close()
        except Exception:
            pass

        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())
