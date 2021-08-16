import bitly_api

BITLY_ACCESS_TOKEN ="4fae9902744ef33f75a12df129858928f6c9b663"

access = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)

full_link = newReferURL(pcode)

short_url = access.shorten(full_link)

context.bot.send_message(chat_id=update.message.chat_id,reply_to_message_id=update.message.message_id, text=short_url)

newReferURL(pcode)
