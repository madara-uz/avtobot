#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights

def print_intro():
    print("=" * 60)
    print("🤖  TELEGRAM GURUHLARI UCHUN BOTLARNI YANGILOVCHI DASTUR")
    print("🔐  Bu dastur faqat o'zingiz EGASI bo‘lgan GURUHLARDA ishlaydi.")
    print("⚙️  Eski botlarni chiqaradi va yangi botlarni admin qiladi.")
    print("📌  Dastur Telethon orqali ishlaydi (Telegram API)")
    print("👨‍💻  Muallif: @originalprofil | GitHub: github.com/YOUR_USERNAME")
    print("=" * 60)

async def main():
    print_intro()

    api_id = int(input("API ID: "))
    api_hash = input("API Hash: ")
    session_name = input("Session nomi (masalan: session1): ")

    new_bots_input = input("➕ Admin qilinadigan yangi botlar (@siz, vergul bilan): ")
    new_bots = [b.strip().lstrip('@') for b in new_bots_input.split(',') if b.strip()]

    old_bots_input = input("➖ Chiqariladigan eski botlar (@siz, vergul bilan yoki bo‘sh qoldiring): ")
    old_bots = [b.strip().lstrip('@') for b in old_bots_input.split(',') if b.strip()]

    async with TelegramClient(session_name, api_id, api_hash) as client:
        me = await client.get_me()
        dialogs = await client.get_dialogs()

        for dialog in dialogs:
            if dialog.is_group:
                chat = dialog.entity
                try:
                    permissions = await client.get_permissions(chat, me.id)
                    if not permissions.is_creator:
                        print(f"⛔️ [{chat.title}] — siz egasi emassiz, o'tkazildi.")
                        continue

                    print(f"\n📁 [{chat.title}] — egalik tasdiqlandi")

                    # ➕ Yangi botlarni admin qilish
                    for bot in new_bots:
                        try:
                            bot_entity = await client.get_entity(bot)
                            rights = ChatAdminRights(
                                change_info=True,
                                post_messages=True,
                                edit_messages=True,
                                delete_messages=True,
                                ban_users=True,
                                invite_users=True,
                                pin_messages=True,
                                add_admins=False,
                                anonymous=False,
                                manage_call=True,
                                manage_topics=True
                            )
                            await client(EditAdminRequest(
                                channel=chat,
                                user_id=bot_entity,
                                admin_rights=rights,
                                rank="AdminBot"
                            ))
                            print(f"[+] @{bot} admin qilindi.")
                        except Exception as e:
                            print(f"[!] @{bot} admin qilishda xato: {e}")

                    # ➖ Eski botlarni chiqarish (agar mavjud bo‘lsa)
                    if old_bots:
                        for bot in old_bots:
                            try:
                                bot_entity = await client.get_entity(bot)
                                ban_rights = ChatBannedRights(
                                    until_date=None,
                                    view_messages=True
                                )
                                await client(EditBannedRequest(
                                    channel=chat,
                                    user_id=bot_entity,
                                    banned_rights=ban_rights
                                ))
                                print(f"[-] @{bot} guruhdan chiqarildi.")
                            except Exception as e:
                                print(f"[!] @{bot} chiqarishda xato: {e}")

                except Exception as e:
                    print(f"[!] [{chat.title}] — umumiy xato: {e}")

if __name__ == "__main__":
    asyncio.run(main())
