# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from datetime import datetime
from django.db import models
from django.db.models.functions import Cast
from django.utils.functional import cached_property


class AndroidMetadata(models.Model):
    locale = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "android_metadata"


class Chat(models.Model):
    chat_id = models.TextField(primary_key=True, blank=True)
    chat_name = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        "app.Contacts",
        null=True,
        on_delete=models.SET_NULL,
        db_column="owner_mid",
        related_name="owned_chats",
    )
    last_from = models.ForeignKey(
        "app.Contacts",
        null=True,
        on_delete=models.SET_NULL,
        db_column="last_from_mid",
        related_name="last_from_chats",
    )
    last_message = models.TextField(blank=True, null=True)
    last_created_time = models.TextField(blank=True, null=True)
    message_count = models.IntegerField(blank=True, null=True)
    read_message_count = models.IntegerField(blank=True, null=True)
    latest_mentioned_position = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    is_notification = models.IntegerField(blank=True, null=True)
    skin_key = models.TextField(blank=True, null=True)
    input_text = models.TextField(blank=True, null=True)
    input_text_metadata = models.TextField(blank=True, null=True)
    hide_member = models.IntegerField(blank=True, null=True)
    p_timer = models.IntegerField(blank=True, null=True)
    last_message_display_time = models.TextField(blank=True, null=True)
    mid_p = models.TextField(blank=True, null=True)
    is_archived = models.IntegerField(blank=True, null=True)
    read_up = models.TextField(blank=True, null=True)
    is_groupcalling = models.IntegerField(blank=True, null=True)
    latest_announcement_seq = models.IntegerField(blank=True, null=True)
    announcement_view_status = models.IntegerField(blank=True, null=True)
    last_message_meta_data = models.TextField(blank=True, null=True)
    chat_room_bgm_data = models.TextField(blank=True, null=True)
    chat_room_bgm_checked = models.IntegerField(blank=True, null=True)
    chat_room_should_show_bgm_badge = models.IntegerField(blank=True, null=True)
    unread_type_and_count = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chat"

    @cached_property
    def history(self):
        created_time_int = Cast(
            "created_time",
            output_field=models.PositiveBigIntegerField(),
        )
        history = self.chat_history.annotate(created_time_int=created_time_int)
        history = history.select_related("from_c")
        history = history.order_by("created_time_int")
        return history

    @cached_property
    def mid_lookup(self):
        return {}

    def get_mid_intish(self, mid):
        try:
            mid_intish = self.mid_lookup[mid]
        except KeyError:
            mid_intish = str(len(self.mid_lookup) + 1)
            self.mid_lookup[mid] = mid_intish
        return mid_intish


class ChatHistory(models.Model):
    server_id = models.TextField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    chat = models.ForeignKey(
        "app.Chat",
        null=True,
        on_delete=models.SET_NULL,
        db_column="chat_id",
        related_name="chat_history",
    )
    from_c = models.ForeignKey(
        "app.Contacts",
        null=True,
        on_delete=models.SET_NULL,
        db_column="from_mid",
        related_name="chat_history",
    )
    content = models.TextField(blank=True, null=True)
    created_time = models.TextField(blank=True, null=True)
    delivered_time = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    sent_count = models.IntegerField(blank=True, null=True)
    read_count = models.IntegerField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    location_address = models.TextField(blank=True, null=True)
    location_phone = models.TextField(blank=True, null=True)
    location_latitude = models.IntegerField(blank=True, null=True)
    location_longitude = models.IntegerField(blank=True, null=True)
    attachement_image = models.IntegerField(blank=True, null=True)
    attachement_image_height = models.IntegerField(blank=True, null=True)
    attachement_image_width = models.IntegerField(blank=True, null=True)
    attachement_image_size = models.IntegerField(blank=True, null=True)
    attachement_type = models.IntegerField(blank=True, null=True)
    attachement_local_uri = models.TextField(blank=True, null=True)
    parameter = models.TextField(blank=True, null=True)
    chunks = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chat_history"

    @cached_property
    def created_at(self):
        if not self.created_time:
            return None
        return datetime.fromtimestamp(int(self.created_time) / 1000)

    @cached_property
    def is_from_self(self):
        return self.from_c_id is None and self.status == 3  # ???

    @cached_property
    def author(self):
        if self.from_c:
            return self.from_c.to_discord(self.chat)
        return {
            "id": self.chat.get_mid_intish(self.from_c_id),
            **Contacts.DEFAULT_DISCORD_PROFILES[
                "self" if self.is_from_self else "unknown"
            ],
        }

    def to_discord(self):
        return {
            # Use created_time as message ID to maintain order,
            # as DCEF sorts by ID rather than timestamp
            "id": self.created_time,
            "type": "Default",
            "timestamp": self.created_at.isoformat(),
            "timestampEdited": None,
            "callEndedTimestamp": None,
            "isPinned": False,
            "content": (self.content or "").strip(),
            "author": self.author,
            "attachments": [],
            "embeds": [],
            "stickers": [],
            "reactions": [],
            "mentions": [],
        }


class ChatMember(models.Model):
    chat = models.ForeignKey(
        "app.Chat",
        null=True,
        on_delete=models.SET_NULL,
        db_column="chat_id",
    )
    contact = models.ForeignKey(
        "app.Contacts",
        null=True,
        on_delete=models.SET_NULL,
        db_column="mid",
    )
    created_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chat_member"
        unique_together = (("chat_id", "contact"),)


class ChatNotification(models.Model):
    chat = models.OneToOneField(
        "app.Chat",
        primary_key=True,
        on_delete=models.CASCADE,
        db_column="chat_id",
    )
    is_notification = models.IntegerField(blank=True, null=True)
    is_groupcalling = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chat_notification"


class Contacts(models.Model):
    m_id = models.TextField(primary_key=True, blank=True)
    contact_id = models.TextField(blank=True, null=True)
    contact_key = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    phonetic_name = models.TextField(blank=True, null=True)
    server_name = models.TextField(blank=True, null=True)
    addressbook_name = models.TextField(blank=True, null=True)
    custom_name = models.TextField(blank=True, null=True)
    status_msg = models.TextField(blank=True, null=True)
    is_unread_status_msg = models.IntegerField(blank=True, null=True)
    picture_status = models.TextField(blank=True, null=True)
    picture_path = models.TextField(blank=True, null=True)
    relation = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    is_first = models.IntegerField(blank=True, null=True)
    capable_flags = models.IntegerField(blank=True, null=True)
    contact_kind = models.IntegerField(blank=True, null=True)
    contact_type = models.IntegerField(blank=True, null=True)
    buddy_category = models.IntegerField(blank=True, null=True)
    buddy_icon_type = models.IntegerField(blank=True, null=True)
    is_on_air = models.IntegerField(blank=True, null=True)
    hidden = models.IntegerField(blank=True, null=True)
    favorite = models.IntegerField(blank=True, null=True)
    updated_time = models.IntegerField(blank=True, null=True)
    created_time = models.IntegerField()
    recommend_params = models.TextField(blank=True, null=True)
    profile_music = models.TextField(blank=True, null=True)
    profile_update_highlight_time = models.IntegerField(blank=True, null=True)
    contact_sync_request_time = models.IntegerField(blank=True, null=True)
    on_air_label = models.IntegerField(blank=True, null=True)
    video_profile = models.TextField(blank=True, null=True)
    schema_ver = models.IntegerField(blank=True, null=True)
    status_msg_meta_data = models.TextField(blank=True, null=True)
    avatar_profile_info = models.TextField(blank=True, null=True)
    friend_ringtone = models.TextField(blank=True, null=True)
    friend_ringbacktone = models.TextField(blank=True, null=True)
    nft_profile = models.IntegerField(blank=True, null=True)
    picture_source = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "contacts"

    @cached_property
    def color(self):
        # Generate color based on the last 6 characters of m_id
        return f"#{self.m_id[-6:]}"

    @cached_property
    def avatar_url(self):
        return self.picture_path

    def to_discord(self, chat=None):
        return {
            "id": chat.get_mid_intish(self.m_id) if chat else 1,
            "name": self.name,
            "discriminator": "0000",
            "nickname": self.custom_name,
            "color": self.color,
            "isBot": False,
            "roles": [],
            "avatarUrl": self.avatar_url,
        }

    DEFAULT_DISCORD_PROFILES = {
        "self": {
            "name": "sage",
            "discriminator": "0000",
            "nickname": "sage",
            "color": "#84cff0",
            "isBot": False,
            "roles": [],
            "avatarUrl": "",
        },
        "unknown": {
            "name": "Unknown",
            "discriminator": "0000",
            "nickname": "Unknown",
            "color": "#ffffff",
            "isBot": False,
            "roles": [],
            "avatarUrl": "",
        },
    }


class GroupHome(models.Model):
    home_id = models.TextField(primary_key=True, blank=True)
    mid = models.TextField(blank=True, null=True)
    is_group = models.IntegerField()
    is_note_newflag = models.IntegerField()
    is_album_newflag = models.IntegerField()
    newflag_expiredtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = "group_home"


class Groups(models.Model):
    id = models.TextField(primary_key=True, blank=True)
    name = models.TextField(blank=True, null=True)
    picture_status = models.TextField(blank=True, null=True)
    creator = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    is_first = models.IntegerField(blank=True, null=True)
    display_type = models.IntegerField(blank=True, null=True)
    accepted_invitation_time = models.IntegerField(blank=True, null=True)
    updated_time = models.IntegerField(blank=True, null=True)
    created_time = models.IntegerField()
    prevented_joinby_ticket = models.IntegerField(blank=True, null=True)
    invitation_ticket = models.TextField(blank=True, null=True)
    favorite_timestamp = models.IntegerField(blank=True, null=True)
    invitation_enabled = models.IntegerField()
    can_add_member_as_friend = models.IntegerField()
    can_invite_by_ticket = models.IntegerField()
    is_auto_name = models.IntegerField()

    class Meta:
        managed = False
        db_table = "groups"

    @cached_property
    def icon_url(self):
        return self.picture_status

    @cached_property
    def chat(self):
        return Chat.objects.get(pk=self.pk)

    def to_discord(self):
        # Ensure unique timestamps. Not ideal, but DCEF sorts
        # by ID rather than timestamp, so we use the timestamp as ID
        # thus we need to ensure they are unique.
        seen_timestamps = set()
        messages = [
            message.to_discord()
            for message in self.chat.history
            if message.created_time not in seen_timestamps
            and not seen_timestamps.add(message.created_time)
        ]
        return {
            "guild": {
                "id": "1",  # must be int-ish
                "name": self.name,
                "iconUrl": self.icon_url,
            },
            "channel": {
                "id": "2",
                "type": "GuildTextChat",
                "categoryId": "703931576941150228",  # ???
                "category": "Text Channels",
                "name": self.name,
                "topic": None,
            },
            "dateRange": {"after": None, "before": None},
            "exportedAt": datetime.now().isoformat(),
            "messages": messages,
            "messageCount": len(messages),
        }


class Membership(models.Model):
    pk = models.CompositePrimaryKey("id", "m_id")
    id = models.TextField()
    m_id = models.TextField()
    is_accepted = models.IntegerField()
    updated_time = models.IntegerField()
    created_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = "membership"


class MoreMenuItemStatus(models.Model):
    parent_id = models.IntegerField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    last_tapped_version = models.IntegerField(blank=True, null=True)
    show_new_badge = models.IntegerField(blank=True, null=True)
    show_tab_badge = models.IntegerField(blank=True, null=True)
    first_displayed_time = models.IntegerField(blank=True, null=True)
    last_tapped_time = models.IntegerField(blank=True, null=True)
    is_used_recently_list = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "more_menu_item_status"


class MultipleImageMessageMapping(models.Model):
    local_message_id = models.AutoField(primary_key=True, blank=True)
    group = models.ForeignKey(
        "app.Groups",
        null=True,
        on_delete=models.SET_NULL,
        db_column="group_id",
    )
    uploading_id = models.IntegerField(blank=True, null=True)
    chat = models.ForeignKey(
        "app.Chat",
        null=True,
        on_delete=models.SET_NULL,
        db_column="chat_id",
    )

    class Meta:
        managed = False
        db_table = "multiple_image_message_mapping"


class MyTheme(models.Model):
    product_id = models.TextField(primary_key=True, blank=True)
    # Field name made lowercase.
    ordernum = models.IntegerField(db_column="orderNum", blank=True, null=True)
    notified_expire_before_2week = models.IntegerField(blank=True, null=True)
    notified_expire_before_1week = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "my_theme"


class PermanentTasks(models.Model):
    task_id = models.AutoField(primary_key=True, blank=True)
    type = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    created_time = models.IntegerField(blank=True, null=True)
    last_executed_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "permanent_tasks"


class Reactions(models.Model):
    # The composite primary key (server_message_id, member_id) found, that is not supported. The first column is selected.
    server_message_id = models.AutoField(primary_key=True)
    member_id = models.TextField()
    chat = models.ForeignKey(
        "app.Chat",
        null=True,
        on_delete=models.SET_NULL,
        db_column="chat_id",
    )
    reaction_time_millis = models.IntegerField()
    reaction_type = models.TextField()

    class Meta:
        managed = False
        db_table = "reactions"


class Setting(models.Model):
    key = models.TextField(primary_key=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "setting"


class Sticker(models.Model):
    sticker_id = models.AutoField(primary_key=True, blank=True)
    package_id = models.IntegerField()
    order_num = models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    popup_align = models.IntegerField(blank=True, null=True)
    popup_scale = models.IntegerField(blank=True, null=True)
    popup_layer = models.IntegerField(blank=True, null=True)
    message_plain_text = models.TextField(blank=True, null=True)
    default_message_plain_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sticker"


class StickerAutoSuggestionTagMap(models.Model):
    package_id = models.IntegerField()
    sticker_id = models.IntegerField()
    tag_id = models.TextField()
    weight = models.FloatField()

    class Meta:
        managed = False
        db_table = "sticker_auto_suggestion_tag_map"


class StickerHistory(models.Model):
    sticker_id = models.IntegerField()
    package_id = models.IntegerField()
    last_used_in_millis = models.IntegerField()
    plain_text = models.TextField()
    weight = models.FloatField()
    combination_sticker_id = models.TextField()

    class Meta:
        managed = False
        db_table = "sticker_history"
        unique_together = (
            ("sticker_id", "package_id", "plain_text", "combination_sticker_id"),
        )


class StickerPackage(models.Model):
    package_id = models.AutoField(primary_key=True, blank=True)
    name = models.TextField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    sticker_type = models.IntegerField(blank=True, null=True)
    sticker_size = models.IntegerField(blank=True, null=True)
    author_id = models.IntegerField(blank=True, null=True)
    is_default = models.IntegerField(blank=True, null=True)
    suggestion_data_revision_millis = models.IntegerField(blank=True, null=True)
    sticker_hash = models.TextField(blank=True, null=True)
    encrypted_text = models.TextField(blank=True, null=True)
    available_for_photo_edit = models.IntegerField(blank=True, null=True)
    is_subscription = models.IntegerField(blank=True, null=True)
    is_show_only = models.IntegerField(blank=True, null=True)
    is_sendable = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    package_status = models.IntegerField(blank=True, null=True)
    expiration_time_millis = models.IntegerField(blank=True, null=True)
    valid_days = models.IntegerField(blank=True, null=True)
    download_status = models.IntegerField(blank=True, null=True)
    download_start_time_millis = models.IntegerField(blank=True, null=True)
    download_complete_time_millis = models.IntegerField(blank=True, null=True)
    install_complete_time_millis = models.IntegerField(blank=True, null=True)
    buddy_mid = models.TextField(blank=True, null=True)
    available_for_combination_sticker = models.IntegerField()

    class Meta:
        managed = False
        db_table = "sticker_package"


class SticonPackages(models.Model):
    sticon_pkg_id = models.AutoField(primary_key=True, blank=True)
    sticon_pkg_ver = models.IntegerField(blank=True, null=True)
    downloaded_sticon_pkg_ver = models.IntegerField(blank=True, null=True)
    meta_data_ver = models.IntegerField(blank=True, null=True)
    downloaded_meta_data_ver = models.IntegerField(blank=True, null=True)
    new_flag_ver = models.IntegerField(blank=True, null=True)
    confirmed_new_flag_ver = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    sticker_pkg_id = models.IntegerField(blank=True, null=True)
    sticker_pkg_ver = models.IntegerField(blank=True, null=True)
    auto_suggestion_data_revision = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sticon_packages"


class Sticons(models.Model):
    sticon_pkg_id = models.IntegerField(blank=True, null=True)
    sticon_code = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    sticker_id = models.IntegerField(blank=True, null=True)
    keyword = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sticons"
        unique_together = (("sticon_pkg_id", "sticon_code"),)


class Version(models.Model):
    contact_id = models.TextField(primary_key=True, blank=True)
    version = models.IntegerField()
    synced_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = "version"
