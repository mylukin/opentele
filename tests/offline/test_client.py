"""Network-free compatibility checks; all credentials and auth keys are synthetic."""
import asyncio
import os

import pytest
from opentele.api import APIData
from opentele.tl import TelegramClient
from telethon.crypto import AuthKey
from telethon.sessions import MemorySession, SQLiteSession
from telethon.tl.functions.help import GetConfigRequest


def test_telethon_positional_credentials_are_preserved():
    async def check():
        client = TelegramClient(MemorySession(), 12345, 'synthetic-api-hash')
        try:
            assert client.api_id == 12345
            assert client.api_hash == 'synthetic-api-hash'
        finally:
            await client.disconnect()
    asyncio.run(check())


def test_independent_client_profiles_serialize_on_current_telethon():
    async def check():
        clients = []
        try:
            for number in (1, 2):
                profile = APIData(
                    api_id=12340 + number, api_hash='synthetic-api-hash',
                    device_model=f'offline-{number}', system_version='test-os',
                    app_version='test-version', lang_code='en',
                    system_lang_code='en-US', lang_pack='tdesktop',
                )
                client = TelegramClient(MemorySession(), api=profile)
                clients.append(client)
            for number, client in enumerate(clients, 1):
                init = client._init_request
                assert init.api_id == 12340 + number
                assert init.device_model == f'offline-{number}'
                assert init.lang_pack == 'tdesktop'
                init.query = GetConfigRequest()
                assert bytes(init)
        finally:
            for client in clients:
                await client.disconnect()
    asyncio.run(check())


def test_sqlite_authorization_survives_close_and_reopen(tmp_path):
    path = str(tmp_path / 'synthetic.session')
    key = os.urandom(256)
    session = SQLiteSession(path)
    session.set_dc(2, '149.154.167.51', 443)
    session.auth_key = AuthKey(key)
    session.save()
    session.close()
    reopened = SQLiteSession(path)
    try:
        assert reopened.auth_key.key == key
        assert reopened.dc_id == 2
    finally:
        reopened.close()


def test_latest_desktop_version_does_not_override_protocol_layer():
    from opentele.api import API
    desktop = API.TelegramDesktop
    # Official v7.3.1 api.tl declares layer 230; Telethon 1.45.0 uses 229.
    assert desktop._versions_for_layer(230) == ['7.3.1']
    assert '7.3.1' not in desktop._versions_for_layer(229)
