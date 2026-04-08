# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Content Moderation Environment Implementation.

"""

from random import choice
from uuid import uuid4
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import ContentModerationAction, ContentModerationObservation
except ImportError:
    from models import ContentModerationAction, ContentModerationObservation


class ContentModerationEnvironment(Environment):
    """
    A Content Moderation environment for evaluating agent decisions.

    The agent receives a post with content, context, and intent, and must decide:
    - allow
    - remove
    - review

    The environment evaluates the decision against a ground-truth label
    and returns a reward between 0.0 and 1.0.

    Each episode consists of a single moderation decision.
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True



    def __init__(self):
        self.data = [
        # EASY
        {
            "content": "This explanation made everything so much easier to understand, really appreciate your effort!",
            "context": "comment on tutorial video",
            "intent": "positive appreciation",
            "label": "allow"
        },
        {
            "content": "People like you are completely useless and should just stay quiet.",
            "context": "toxic argument online",
            "intent": "direct insult",
            "label": "remove"
        },
      {
    "content": "I really liked how you approached this problem, very creative thinking.",
    "context": "peer feedback discussion",
    "intent": "constructive praise",
    "label": "allow"
    },

        # MEDIUM
        {
            "content": "This is honestly a very poor attempt, you clearly don't understand the basics.",
            "context": "feedback after submission",
            "intent": "harsh criticism",
            "label": "review"
        },
        {
            "content": "You're actually terrible at this, maybe this isn't for you.",
            "context": "after someone performs badly",
            "intent": "demeaning insult",
            "label": "remove"
        },
        {
        "content": "You're insane, that move was unbelievable!",
        "context": "reaction to gaming highlight",
        "intent": "positive slang praise",
        "label": "allow"
        },
        {
        "content": "I think your solution has some mistakes, maybe you can review the logic again.",
        "context": "code review discussion",
        "intent": "constructive criticism",
        "label": "allow"
        },

        # HARD
        {
            "content": "Wow, that was a genius move… really impressive 🙄",
            "context": "after obvious mistake in discussion",
            "intent": "sarcastic insult",
            "label": "review"
        },
        {
            "content": "If you mess this up again, I swear I'll kill you 😂 relax I'm joking",
            "context": "friends joking during online game",
            "intent": "joking with violent language",
            "label": "review"
        },
        {
        "content": "This track is absolutely sick, I've had it on repeat all day.",
        "context": "music appreciation post",
        "intent": "positive slang",
        "label": "allow"
        },
        {
        "content": "I will track you down even if you think this is a joke.",
        "context": "ambiguous but escalating",
        "intent": "threat",
        "label": "remove"
        }
    ]
        self.current = None
        self._state = State(episode_id=str(uuid4()), step_count=0)
        
    def reset(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current = choice(self.data)

        return ContentModerationObservation(
        content=self.current["content"],
        context=self.current.get("context"),
        intent=self.current.get("intent"),
        reward=0.0,
        done=False,
        metadata={}
    )

    def step(self, action: ContentModerationAction):
        self._state.step_count += 1

        correct = self.current["label"]

        if action.decision == correct:
            reward = 1.0
        elif action.decision == "review":
            reward = 0.5
        else:
            reward = 0.0

        return ContentModerationObservation(
        content=self.current["content"],
        context=self.current.get("context"),
        intent=self.current.get("intent"),
        reward=reward,
        done=True,
        metadata={"correct_label": correct}
    )
    @property
    def state(self) -> State:
        
        return self._state
