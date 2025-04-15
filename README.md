# Telegram Media Transfer Bot

Automatically transfers media files from a source channel to a target channel, uploading them as videos.

## Features

- Downloads media from source channel using message link
- Uploads all media as videos (not documents)
- Supports streaming
- No captions in transferred media
- Fully automated (no user input required)
- Handles rate limits automatically
- Shows progress and statistics

## Deployment on Koyeb

1. Fork this repository to your GitHub account

2. Sign up for a Koyeb account at https://app.koyeb.com

3. In Koyeb, create a new app:
   - Click "Create App"
   - Choose "GitHub" as the deployment method
   - Select your forked repository
   - Choose the main branch

4. Configure environment variables in Koyeb:
   - `API_ID` - Your Telegram API ID
   - `API_HASH` - Your Telegram API Hash
   - `SOURCE_MESSAGE_LINK` - Link to any message in the source channel (e.g., https://t.me/c/1234567890/1)
   - `TARGET_CHANNEL` - Target channel ID (e.g., -1001234567890)

5. Deploy the app:
   - Choose "Docker" as the runtime
   - Set the port to 80
   - Click "Deploy"

## Important Notes

1. Make sure the bot account:
   - Is a member of both source and target channels
   - Has permission to read messages in the source channel
   - Has permission to send messages in the target channel

2. The bot will:
   - Start transferring files automatically
   - Handle rate limits by waiting when needed
   - Continue from where it left off if restarted

3. Monitor the progress in Koyeb logs

## Getting Channel IDs and API Credentials

1. API Credentials:
   - Go to https://my.telegram.org/auth
   - Log in and go to "API development tools"
   - Create an app and copy API_ID and API_HASH

2. Channel IDs:
   - Forward a message from the channel to @username_to_id_bot
   - Use the ID with -100 prefix for the TARGET_CHANNEL

3. Source Message Link:
   - Open any message in the source channel
   - Copy the message link
   - Use this as SOURCE_MESSAGE_LINK 