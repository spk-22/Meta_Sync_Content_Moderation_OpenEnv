# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Content Moderation Environment.

The content_moderation environment is a simple test environment that echoes back messages.
"""



from openenv.core.env_server.types import Action, Observation
from pydantic import Field
from typing import Optional

class ContentModerationAction(Action):
    decision: str = Field(..., description="allow | remove | review")


class ContentModerationObservation(Observation):
    content: str = Field(..., description="The post text")
    context: Optional[str] = Field(None, description="Context of the post")
    intent: Optional[str] = Field(None, description="Underlying intent")

