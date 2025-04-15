import os
import asyncio
import re
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, Channel
from telethon.errors import FloodWaitError, ChatAdminRequiredError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram API credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SOURCE_MESSAGE_LINK = os.getenv('SOURCE_MESSAGE_LINK')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')

# Initialize the client
client = TelegramClient('media_transfer_session', API_ID, API_HASH)

async def get_channel_from_message_link(message_link):
    """Extract channel information from a message link"""
    try:
        # Parse the message link to get channel info
        # Format: https://t.me/c/channel_id/message_id or https://t.me/username/message_id
        if not message_link:
            print("No message link provided")
            return None
            
        print(f"Processing message link: {message_link}")
        
        # Extract channel info from the message link
        if '/c/' in message_link:
            # Private channel format: https://t.me/c/channel_id/message_id
            parts = message_link.split('/c/')[1].split('/')
            if len(parts) >= 2:
                channel_id = int(parts[0])
                message_id = int(parts[1])
                print(f"Extracted channel ID: {channel_id}, message ID: {message_id}")
                
                try:
                    # Try to get the channel directly
                    channel = await client.get_entity(channel_id)
                    print(f"Found source channel: {channel.title}")
                    return channel
                except Exception as e:
                    print(f"Error getting channel by ID: {str(e)}")
                    
                    # Try to find in dialogs
                    async for dialog in client.iter_dialogs():
                        if isinstance(dialog.entity, Channel) and dialog.entity.id == channel_id:
                            print(f"Found source channel in dialogs: {dialog.title}")
                            return dialog.entity
        else:
            # Public channel format: https://t.me/username/message_id
            parts = message_link.split('/')
            if len(parts) >= 4:
                username = parts[3]
                message_id = int(parts[4]) if len(parts) > 4 else None
                print(f"Extracted username: {username}, message ID: {message_id}")
                
                try:
                    # Try to get the channel by username
                    channel = await client.get_entity(username)
                    print(f"Found source channel: {channel.title}")
                    return channel
                except Exception as e:
                    print(f"Error getting channel by username: {str(e)}")
                    
                    # Try to find in dialogs
                    async for dialog in client.iter_dialogs():
                        if isinstance(dialog.entity, Channel) and dialog.entity.username == username:
                            print(f"Found source channel in dialogs: {dialog.title}")
                            return dialog.entity
        
        print("Could not find the source channel from the message link")
        return None
        
    except Exception as e:
        print(f"Error processing message link: {str(e)}")
        return None

async def get_target_channel():
    try:
        # Try to get the target channel directly
        try:
            # Convert string ID to integer if it's a numeric ID
            if TARGET_CHANNEL.startswith('-100'):
                channel_id = int(TARGET_CHANNEL)
                return await client.get_entity(channel_id)
            else:
                return await client.get_entity(TARGET_CHANNEL)
        except Exception as e:
            print(f"Error getting target channel directly: {str(e)}")
            
        # If direct access fails, try to find it in dialogs
        async for dialog in client.iter_dialogs():
            if isinstance(dialog.entity, Channel):
                try:
                    if str(dialog.entity.id) == TARGET_CHANNEL or dialog.entity.title == TARGET_CHANNEL:
                        print(f"Found target channel: {dialog.title}")
                        return dialog.entity
                except:
                    continue
                    
        print(f"Could not find target channel with ID/name: {TARGET_CHANNEL}")
        return None
    except Exception as e:
        print(f"Error getting target channel: {str(e)}")
        return None

async def count_media_files(channel):
    """Count the total number of media files in the channel"""
    media_count = 0
    print("Counting media files in the channel...")
    
    async for message in client.iter_messages(channel):
        if message.media:
            media_count += 1
            
    return media_count

async def download_and_upload_media():
    try:
        # Connect to Telegram
        await client.start()
        print("Connected to Telegram successfully!")

        # Get the source channel from message link
        source_channel = await get_channel_from_message_link(SOURCE_MESSAGE_LINK)
        if not source_channel:
            print("Failed to access source channel. Exiting...")
            return

        # Get the target channel entity
        target_channel = await get_target_channel()
        if not target_channel:
            print("Failed to access target channel. Exiting...")
            return

        print(f"Starting media transfer from {source_channel.title} to {target_channel.title}")

        # Get total message count
        total_messages = await client.get_messages(source_channel, limit=0)
        print(f"Total messages in channel: {total_messages.total}")
        
        # Count total media files
        total_media = await count_media_files(source_channel)
        print(f"Total media files to transfer: {total_media}")
        
        if total_media == 0:
            print("No media files found in the channel. Exiting...")
            return
            
        # No confirmation needed - start transfer automatically
        print(f"Starting transfer of {total_media} media files from {source_channel.title} to {target_channel.title}")

        # Counter for transferred media
        transferred_count = 0

        # Get all messages from the source channel, oldest first
        async for message in client.iter_messages(source_channel, reverse=True):  # Changed to reverse=True for oldest first
            if message.media:
                try:
                    # Download the media
                    print(f"Downloading media from message {message.id} (oldest first)")  # Updated log message
                    path = await message.download_media()
                    
                    if path:
                        # Upload the media to target channel as video
                        print(f"Uploading media to target channel")
                        await client.send_file(
                            target_channel,
                            path,
                            force_document=False,  # This ensures it's sent as media
                            video=True,  # This ensures it's treated as video
                            supports_streaming=True,  # Enable streaming for videos
                            caption="",
                            thumb=None  # Let Telegram generate thumbnail
                        )
                        
                        # Clean up downloaded file
                        os.remove(path)
                        transferred_count += 1
                        print(f"Successfully transferred media from message {message.id} ({transferred_count}/{total_media})")
                        
                except FloodWaitError as e:
                    print(f"FloodWaitError: Need to wait {e.seconds} seconds")
                    await asyncio.sleep(e.seconds)
                    continue
                except Exception as e:
                    print(f"Error processing message {message.id}: {str(e)}")
                    continue

        print(f"Transfer completed! Transferred {transferred_count} out of {total_media} media files.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(download_and_upload_media()) 