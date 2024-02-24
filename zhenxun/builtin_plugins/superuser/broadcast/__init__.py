from typing import Annotated

from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.params import Command
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig, Task
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

from ._data_source import BroadcastManage

__plugin_meta__ = PluginMetadata(
    name="广播",
    description="昭告天下！",
    usage="""
    广播 [消息] [图片]
    示例：广播 你们好！
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
        configs=[
            RegisterConfig(
                module="_task",
                key="DEFAULT_BROADCAST",
                value=True,
                help="被动 广播 进群默认开关状态",
                default_value=True,
                type=bool,
            )
        ],
        tasks=[Task(module="broadcast", name="广播")],
    ).dict(),
)

_matcher = on_command("广播", priority=1, permission=SUPERUSER, block=True)


@_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    message: UniMsg,
    command: Annotated[tuple[str, ...], Command()],
):
    message[0].text = message[0].text.replace(command[0], "").strip()
    # await Text("正在发送..请等一下哦!").send()
    count, error_count = await BroadcastManage.send(bot, message, session)
    result = f"成功广播 {count} 个群组"
    if error_count:
        result += f"\n广播失败 {error_count} 个群组"
    await Text(f"发送广播完成!\n{result}").send(reply=True)
    logger.info(f"发送广播信息: {message}", "广播", session=session)
