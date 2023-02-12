from typing import Set

import pytest
from nonebot.plugin import Plugin
from utils import make_fake_event

from nonebug import App


@pytest.mark.asyncio
async def test_process(app: App, load_plugin: Set[Plugin]):
    from tests.plugins.process import (
        test,
        test_ignore,
        test_not_pass_perm,
        test_not_pass_rule,
    )

    # test
    async with app.test_matcher() as ctx:
        adapter = ctx.create_adapter()
        bot = ctx.create_bot(adapter=adapter)

        event = make_fake_event()()
        ctx.receive_event(bot, event)

        ctx.should_pass_permission(matcher=test)
        ctx.should_pass_rule(matcher=test)
        ctx.should_not_pass_permission(matcher=test_not_pass_perm)
        ctx.should_pass_permission(matcher=test_not_pass_rule)
        ctx.should_not_pass_rule(matcher=test_not_pass_rule)
        ctx.should_ignore_permission()
        ctx.should_not_pass_rule()

        ctx.should_call_send(event, "test_send", "result", bot=bot)
        ctx.should_call_api("test", {"key": "value"}, "result", adapter=adapter)
        ctx.should_paused(matcher=test)

        event = make_fake_event()()
        ctx.receive_event(bot, event)

        ctx.should_pass_permission(matcher=test)
        ctx.should_pass_rule(matcher=test)

        ctx.should_rejected(matcher=test)

    # test ignore
    async with app.test_matcher(test_ignore) as ctx:
        adapter = ctx.create_adapter()
        bot = ctx.create_bot(adapter=adapter)

        event = make_fake_event()()
        ctx.receive_event(bot, event)

        ctx.should_ignore_permission()
        ctx.should_ignore_rule()

        ctx.should_call_send(event, "key", "result", bot=bot)
        ctx.should_rejected()

        event = make_fake_event()()
        ctx.receive_event(bot, event)

        ctx.should_pass_permission()
        ctx.should_pass_rule()

        ctx.should_call_send(event, "message", "result", bot=bot)
        ctx.should_finished()
