# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


"""Content Moderation Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import ContentModerationAction, ContentModerationObservation


class ContentModerationEnv(
    EnvClient[ContentModerationAction, ContentModerationObservation, State]
):
    """
    Client for the Content Moderation Environment.
    """

    def _step_payload(self, action: ContentModerationAction) -> Dict:
        """
        Convert ContentModerationAction to JSON payload for step message.
        """
        return {
            "decision": action.decision,   # ✅ FIXED
        }

    def _parse_result(self, payload: Dict) -> StepResult[ContentModerationObservation]:
        """
        Parse server response into StepResult.
        """
        obs_data = payload.get("observation", {})  # ✅ FIXED

        observation = ContentModerationObservation(
            content=obs_data.get("content"),       # ✅ FIXED
            context=obs_data.get("context"),
            intent=obs_data.get("intent"),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )