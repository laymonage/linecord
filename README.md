# linecord

Export your [LINE](https://line.me) chat history to [Discord](https://discord.com)-compatible format.

1. Install the dependencies from pyproject.toml.
2. Copy your `naver_line` SQLite database as `db.sqlite3` to the root of this project.
   - Can be obtained from `/data/data/jp.naver.line.android/databases/`, needs root.
3. Run `python manage.py export {groupname}`.
4. Use the exported `groupname.json` for something like [DiscordChatExporter-frontend](https://github.com/slatinsky/DiscordChatExporter-frontend)

Only group chats are supported, but it should be possible to support other chat rooms. Only basic text is supported - no images or replies yet. I have no plans to develop this further other than for my own needs, so use at your own risk.
