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
- Downloads from oldest to newest messages

## Deployment on Koyeb

### Method 1: Using GitHub

1. Fork this repository to your GitHub account

2. Sign up for a Koyeb account at https://app.koyeb.com

3. In Koyeb, create a new app:
   - Click "Create App"
   - Choose "GitHub" as the deployment method
   - Select your forked repository
   - Choose the main branch

4. Configure environment variables in Koyeb:
   - `API_ID` - Your Telegram API ID (must be a number, e.g., "123456")
   - `API_HASH` - Your Telegram API Hash (32-character string, e.g., "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")
   - `SOURCE_MESSAGE_LINK` - Link to any message in the source channel (e.g., https://t.me/c/1234567890/1)
   - `TARGET_CHANNEL` - Target channel ID (must be a number with -100 prefix, e.g., "-1001234567890")

   ⚠️ Important: Make sure to:
   - Remove any quotes around the values
   - Use the exact format shown in the examples
   - For TARGET_CHANNEL, include the -100 prefix
   - For API_ID, use only numbers

5. Deploy the app:
   - Choose "Docker" as the runtime
   - Set the port to 80
   - Click "Deploy"

### Method 2: Using Docker Image

1. Build the Docker image locally:
   ```bash
   docker build -t telegram-media-transfer .
   ```

2. Push to Docker Hub:
   ```bash
   docker tag telegram-media-transfer yourusername/telegram-media-transfer
   docker push yourusername/telegram-media-transfer
   ```

3. In Koyeb, create a new app:
   - Click "Create App"
   - Choose "Docker" as the deployment method
   - Enter your Docker image: `yourusername/telegram-media-transfer`

4. Configure environment variables in Koyeb:
   - `API_ID` - Your Telegram API ID
   - `API_HASH` - Your Telegram API Hash
   - `SOURCE_MESSAGE_LINK` - Link to any message in the source channel
   - `TARGET_CHANNEL` - Target channel ID

5. Deploy the app

## Important Notes

1. Make sure the bot account:
   - Is a member of both source and target channels
   - Has permission to read messages in the source channel
   - Has permission to send messages in the target channel

2. The bot will:
   - Start transferring files automatically
   - Handle rate limits by waiting when needed
   - Continue from where it left off if restarted
   - Download all media files from oldest to newest

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

## Troubleshooting

If you encounter issues with the deployment:

1. Check the Koyeb logs for error messages
2. Verify that all environment variables are set correctly
3. Make sure the bot account has the necessary permissions
4. Try running the script locally first to ensure it works 