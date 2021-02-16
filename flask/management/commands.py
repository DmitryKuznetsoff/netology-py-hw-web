import asyncio
from email.message import EmailMessage

import aiosmtplib
from dotenv import load_dotenv

from app.config import Config
from user.models import User

load_dotenv()


def mailing_command():
    def create_msg(user: User):
        msg = EmailMessage()
        msg['From'] = Config.ADMIN_EMAIL_LOGIN
        msg['To'] = user.email
        msg['Header'] = 'some header'
        msg.set_content(f'hi, {user.username}!\nthis is some test email content')
        return msg

    async def get_msg_tasks():
        tbl = User.__table__
        async with Config.AIOPG_ENGINE as engine:
            async with engine.acquire() as conn:
                msgs = [create_msg(user) async for user in await conn.execute(tbl.select())]
                if msgs:
                    tasks = [send_msg(msg) for msg in msgs]
                    await asyncio.gather(*tasks)

    async def send_msg(message) -> None:
        await aiosmtplib.send(
            message=message,
            hostname=Config.SMTP_HOST,
            port=Config.SMTP_PORT,
            username=Config.ADMIN_EMAIL_LOGIN,
            password=Config.ADMIN_EMAIL_PWD,
            use_tls=True
        )

    asyncio.get_event_loop()
    asyncio.run(get_msg_tasks())
