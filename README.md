# PnP_GPT Bot

PnP_GPT is a Discord bot designed to assist users on the Pride & Pixels server, a community for LGBT Youth Scotland (LGBTYS).

## Features

- Responds to user queries using OpenAI's GPT model.
- Monitors messages for banned words and deletes inappropriate content.
- Provides concise and helpful responses.

## Setup

1. **Install dependencies:**
    ```bash
    pip install discord aiofiles openai
    ```

2. **Configuration:**
    - Place your OpenAI API key in `openai.priv`.
    - Place your Discord bot token in `bot.priv`.
    - Add banned words in `banned_words.txt`.
    - Customize the system message in `system_message.txt`.

3. **Run the bot:**
    ```bash
    python pnp_gpt_bot.py
    ```

## Usage

- Use the `/ask` command to interact with the bot.
- The bot will automatically monitor and delete messages containing banned words.

## Contact
For any inquiries, please contact the author directly via github or email:
[laura.e.git@pm.me](mailto:laura.e.git@pm.me)