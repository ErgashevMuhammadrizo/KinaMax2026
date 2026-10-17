#!/usr/bin/env python3
"""
Majburiy obuna linklar testlari
"""

from services.subscription import build_subscription_keyboard

# Test data
test_subs = [
    {
        'channel_id': '-1001234567890',
        'channel_title': 'Test Public Channel',
        'channel_username': '@test_channel'
    },
    {
        'channel_id': '-1009876543210',
        'channel_title': 'Test Private Channel',
        'channel_username': None
    }
]

print("=" * 60)
print("🧪 SUBSCRIPTION LINKS TEST")
print("=" * 60)

kb = build_subscription_keyboard(test_subs)

print("\n✅ Generated keyboard buttons:\n")
for i, row in enumerate(kb.inline_keyboard, 1):
    for btn in row:
        if hasattr(btn, 'url') and btn.url:
            print(f"{i}. {btn.text}")
            print(f"   URL: {btn.url}")
        else:
            print(f"{i}. {btn.text}")
            print(f"   Callback: {btn.callback_data}")
        print()

print("=" * 60)
print("✅ Test muvaffaqiyatli!")
print("=" * 60)
