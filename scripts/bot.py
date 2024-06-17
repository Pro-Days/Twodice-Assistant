import os
import misc
import random
import discord
import platform
import datetime
from pytz import timezone
import get_rank_info as gri
import register_player as rp
import get_server_info as gsi
import get_character_info as gci

os_name = platform.system()
if os_name == "Linux":
    LOG_CHANNEL_ID = 1244676938002468939
    ADMIN_CHANNEL_ID = 1244674283826053241
    ADMIN_ID = 407775594714103808
else:
    LOG_CHANNEL_ID = 1248628675134488637
    ADMIN_CHANNEL_ID = 1248628536311550045
    ADMIN_ID = 407775594714103808


class DiscordBot:
    def __init__(self, discord_client):
        self.discord_client = discord_client

    async def admin(self, message):
        msg = message.content

        if msg == "stop":
            await self.send("종료합니다.", message, log_type=4)
            await self.send_log(log_type=2)
            print("디스코드 로그아웃 시작")
            await self.discord_client.close()

            return

        elif msg == "ip":
            ip = misc.get_ip()
            await self.send(f"아이피 주소: {ip}", message, log_type=4)

            return

        elif msg == "user_list":
            pl_list = rp.registered_player_list()

            msg = (
                f"등록된 유저 수: {len(pl_list)}\n등록된 유저 목록\n"
                + "```"
                + ", ".join(pl_list)
                + "```"
            )

            await self.send(msg, message, log_type=4)

            return

        elif msg == "server_list":
            pl_list = rp.registered_player_list()

            msg = (
                f"서버 수: {str(len(self.discord_client.guilds))}\n서버 목록\n"
                + "```"
                + ", ".join([guild.name for guild in self.discord_client.guilds])
                + "```"
            )

            await self.send(msg, message, log_type=4)

            return

        elif msg == "cmd":
            await self.send(
                "1. stop\n2. ip\n3. user_list\n4. server_list\n5. cmd",
                message,
                log_type=4,
            )

            return

    async def hanwol(self, message, ans_json):
        """
        fn_id: -1 - 일반 메시지
        fn_id: 1 - 서버 정보
        fn_id: 2 - 랭킹 정보
        fn_id: 3 - 캐릭터 정보
        fn_id: 4 - 캐릭터 등록
        """

        msg = message.content[4:]

        if ans_json["fn_id"] == -1:
            await self.send(
                ans_json["text"],
                message,
                ans_json,
            )

            return

        elif ans_json["fn_id"] == 1:
            temp_message = await self.send_temp_message(message)

            period = ans_json["var"]["period"] if "period" in ans_json["var"] else 7

            msg, image = gsi.get_server_info(period)

            await self.send(
                msg,
                message,
                ans_json,
                image=image,
                temp_message=temp_message,
            )

            return

        elif ans_json["fn_id"] == 2:
            temp_message = await self.send_temp_message(message)

            if "page" in ans_json["var"]:
                page = int(ans_json["var"]["page"])
            else:
                page = 1  # 1~
            image = gri.get_rank_info(page)

            if image == None:
                if page != 1:
                    msg = [
                        f"죄송하지만 {page}페이지의 랭킹 정보를 불러올 수 없어요.",
                        f"죄송해요. {page}페이지의 랭킹 정보는 알려드릴 수 없어요.",
                        f"죄송하지만 {page}페이지의 랭킹 데이터를 가져올 수 없어요.",
                        f"죄송해요. {page}페이지의 랭킹 정보를 찾을 수 없어요.",
                        f"죄송해요. {page}페이지의 랭킹 정보를 불러오는데 실패했어요.",
                        f"죄송하지만 {page}페이지의 랭킹 정보를 불러오는 데 문제가 발생했어요.",
                    ]

                else:
                    msg = [
                        "죄송하지만 현재 랭킹 정보를 불러올 수 없어요.",
                        "죄송하지만 지금은 랭킹 데이터를 가져올 수 없어요.",
                        "죄송해요. 랭킹 정보를 불러오는데 실패했어요.",
                        "죄송하지만 랭킹 정보를 불러오는 데 문제가 발생했어요.",
                    ]
                await self.send(
                    random.choice(msg),
                    message,
                    ans_json,
                    temp_message=temp_message,
                )

                return

            if page == 1:
                msg = [
                    f"한월 서버의 캐릭터 레벨 랭킹을 보여드릴게요.",
                    f"한월 서버의 캐릭터 랭킹을 알려드릴게요.",
                    f"지금 한월 서버의 캐릭터 랭킹은 다음과 같아요.",
                    f"한월 서버의 레벨 순위를 보여드릴게요.",
                    f"지금 한월의 레벨 랭킹을 보여드릴게요.",
                ]

            else:
                msg = [
                    f"한월 서버의 {page}페이지 캐릭터 레벨 랭킹을 보여드릴게요.",
                    f"한월 서버의 {page}페이지 레벨 랭킹을 알려드릴게요.",
                    f"이 이미지는 지금 한월 서버의 {page}페이지 캐릭터 랭킹이에요.",
                    f"아래 이미지는 한월 서버의 {page}페이지 캐릭터 순위에요.",
                    f"지금 한월의 {page}페이지 레벨 랭킹을 보여드릴게요.",
                ]

            await self.send(
                random.choice(msg),
                message,
                ans_json,
                image=image,
                temp_message=temp_message,
            )

            return

        elif ans_json["fn_id"] == 3:
            temp_message = await self.send_temp_message(message)

            name = ans_json["var"]["name"]
            if "slot" in ans_json["var"]:
                slot = ans_json["var"]["slot"]
                default = False

            else:
                slot = rp.get_main_slot(name)  # 1~3
                default = True

            period = ans_json["var"]["period"] if "period" in ans_json["var"] else 7

            if not rp.is_registered(name):
                """셀레니움으로 크롤링해서 현재 캐릭터 정보 가져오기"""
                msg = [
                    "그 플레이어는 등록되지 않았어요.",
                    "해당 플레이어는 등록되어 있지 않아요.",
                    "말씀하신 플레이어는 등록되지 않았어요.",
                    "해당 플레이어는 목록에 등록되어 있지 않아요.",
                    "찾으시는 플레이어는 등록되지 않았어요.",
                ]
                await self.send(
                    random.choice(msg),
                    message,
                    ans_json,
                    temp_message=temp_message,
                )

                return

            msg, image = gci.get_character_info(
                name, slot, period=period, default=default
            )
            await self.send(
                msg,
                message,
                ans_json,
                image=image,
                temp_message=temp_message,
            )

            return

        elif ans_json["fn_id"] == 4:
            temp_message = await self.send_temp_message(message)

            name = ans_json["var"]["name"]

            if "slot" in ans_json["var"]:
                slot = int(ans_json["var"]["slot"])

            else:
                slot = 1

            rp.register_player(name, slot)

            name = misc.get_real_name(name)
            msg = [
                f"{name} 캐릭터를 메인 슬롯 {slot}번으로 등록했어요!",
                f"{name} 등록 완료! 메인 슬롯은 {slot}번으로 설정했어요.",
                f"메인슬롯 {slot}번으로 {name} 캐릭터 등록에 성공했어요.",
            ]
            msg = random.choice(msg)

            if msg.count("_") >= 2:
                msg += "\n실제로는 언더바(_)가 정상적으로 적용되니 걱정마세요!"

            await self.send(msg, message, ans_json, temp_message=temp_message)

            return

    async def send_temp_message(self, message):
        temp_message = await message.reply("잠시 기다려주세요.", mention_author=True)
        await self.send_log(6, var=(message))

        return temp_message

    async def send(
        self,
        msg,
        message,
        ans_json=None,
        image=None,
        log_type=3,
        error=None,
        temp_message=None,
    ):
        if temp_message != None:
            await temp_message.delete()

        if image == None:
            await message.reply(msg, mention_author=True)
            # await channel.send(msg)
            await self.send_log(
                log_type,
                var=(message, ans_json, msg, image, error),
            )

            return

        await message.reply(msg, file=discord.File(image), mention_author=True)
        # await channel.send(msg, file=discord.File(image))
        await self.send_log(log_type, var=(message, ans_json, msg, image, error))
        os.remove(image)

    async def send_log(self, log_type, var=None):
        """
        log_type: 1 - 로그인
        log_type: 2 - 로그아웃
        log_type: 3 - 명령어 로그
        log_type: 4 - 관리자 명령어 로그
        log_type: 5 - 명령어 에러 로그
        log_type: 6 - 임시 메시지 로그
        """

        if log_type == 1:
            embed = discord.Embed()
            embed.title = "투다이스 어시스턴트 로그인"
            embed.color = discord.Color.green()

            embed_json = {
                "time": datetime.datetime.now(timezone("Asia/Seoul")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "ip": misc.get_ip(),
                "server_count": str(len(self.discord_client.guilds)),
                "server_list": "```"
                + ", ".join([guild.name for guild in self.discord_client.guilds])
                + "```",
                "user_count": str(len(self.discord_client.users)),
                "user_list": "```"
                + ", ".join([user.name for user in self.discord_client.users])
                + "```",
            }

            for key, value in embed_json.items():
                if value != None:
                    embed.add_field(
                        name=key,
                        value=value,
                        inline=False,
                    )

            await self.discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

        elif log_type == 2:
            embed = discord.Embed()
            embed.title = "투다이스 어시스턴트 로그아웃"
            embed.color = discord.Color.orange()

            embed_json = {
                "time": datetime.datetime.now(timezone("Asia/Seoul")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }

            for key, value in embed_json.items():
                if value != None:
                    embed.add_field(
                        name=key,
                        value=value,
                        inline=False,
                    )

            await self.discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

        elif (log_type == 3) or (log_type == 4):
            message, ans_json, msg, image, error = var
            guild = await self.discord_client.fetch_guild(message.guild.id)
            member = await guild.fetch_member(message.author.id)
            embed_json = {
                "time": datetime.datetime.now(timezone("Asia/Seoul")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "server": message.guild.name,
                "channel": message.channel.mention,
                "author": f"{member.display_name} ({message.author.name})",
                "text": message.content,
                "ans_json": ans_json,
                "msg": msg,
            }

            embed = discord.Embed()
            if log_type == 3:
                embed.title = "투다이스 어시스턴트 명령어 로그"
                embed.color = discord.Color.blue()

            elif log_type == 4:
                embed.title = "투다이스 어시스턴트 관리자 명령어 로그"
                embed.color = discord.Color.purple()

            for key, value in embed_json.items():
                if value != None:
                    embed.add_field(
                        name=key,
                        value=value,
                        inline=False,
                    )

            await self.discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

            if image == None:
                return

            await self.discord_client.get_channel(LOG_CHANNEL_ID).send(
                file=discord.File(image)
            )

        elif log_type == 5:
            message, ans_json, msg, image, error = var
            guild = await self.discord_client.fetch_guild(message.guild.id)
            member = await guild.fetch_member(message.author.id)
            embed_json = {
                "time": datetime.datetime.now(timezone("Asia/Seoul")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "server": message.guild.name,
                "channel": message.channel.mention,
                "author": f"{member.display_name} ({message.author.name})",
                "text": message.content,
                "ans_json": ans_json,
                "msg": msg,
                "error": error,
            }

            embed = discord.Embed()
            embed.title = "투다이스 어시스턴트 명령어 에러 로그"
            embed.description = f"<@{ADMIN_ID}>"
            embed.color = discord.Color.red()

            for key, value in embed_json.items():
                if value != None:
                    embed.add_field(
                        name=key,
                        value=value,
                        inline=False,
                    )

            await self.discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

        elif log_type == 6:
            message = var
            guild = await self.discord_client.fetch_guild(message.guild.id)
            member = await guild.fetch_member(message.author.id)
            embed_json = {
                "time": datetime.datetime.now(timezone("Asia/Seoul")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "server": message.guild.name,
                "channel": message.channel.mention,
                "author": f"{member.display_name} ({message.author.name})",
                "text": message.content,
            }

            embed = discord.Embed()
            embed.title = "투다이스 어시스턴트 임시 메시지 로그"
            embed.color = discord.Color.dark_grey()

            for key, value in embed_json.items():
                if value != None:
                    embed.add_field(
                        name=key,
                        value=value,
                        inline=False,
                    )

            await self.discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)
