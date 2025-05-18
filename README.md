# Discord Emoji Usage Bot

This is a Discord bot that tracks the usage of custom emojis in messages, stores daily counts in a JSON file, and generates a bar graph of the top emojis used over the last 30 days when the `!emojusage` command is used. Built with Python, discord.py, and matplotlib.

## Setup

1. Install dependencies:
   ```command prompt
   pip install discord.py matplotlib numpy
   ```

2. Replace `'your_bot_token_here'` in the code's last line with your actual Discord bot token.

3. Run the bot:
   ```command prompt
   python bot.py
   ```

## Functionality

- Tracks custom emoji usage in messages and stores daily counts in `emoji_usage.json`.
- Uses the `!emojusage` command to generate a horizontal bar graph of the top emojis (up to 50) used in the last 30 days.
- Displays emoji names and usage counts on the graph.
- Timestamps are in Bangladesh timezone (Asia/Dhaka).
- Saves the graph as a PNG, sends it to the channel, and deletes the file after sending.

## Requirements

- Python 3.8+
- discord.py
- matplotlib
- numpy

## Usage

- The bot automatically tracks custom emojis in messages.
- Use the `!emojusage` command in a channel to generate and receive the emoji usage graph.

## Notes

- Ensure the bot has permissions to read messages, access emojis, and send files in channels.
- The bot requires access to the guild's emojis to display their names in the graph.
- Data is stored in `emoji_usage.json` in the project directory.
