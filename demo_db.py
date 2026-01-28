# This script demonstrates how to save and read data in SQLite using Django

import os
import django

# Setup Django environment manually (since we are running this as a standalone script)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remdesk_project.settings')
django.setup()

from core.models import ContactMessage

print("----------------------------------------------------------------")
print("STEP 1: Saving a new record to SQLite...")
print("----------------------------------------------------------------")

# Create a new ContactMessage object
# This is like writing a row in a spreadsheet or SQL INSERT
new_message = ContactMessage(
    name="Demo User",
    email="demo@example.com",
    message="This is a test message to show that SQLite is working!"
)

# Save it to the database
new_message.save()

print(f"✅ Success! Saved message with ID: {new_message.id}")
print(f"   Name: {new_message.name}")
print(f"   Message: {new_message.message}")


print("\n----------------------------------------------------------------")
print("STEP 2: Reading back from SQLite...")
print("----------------------------------------------------------------")

# Retrieve records
# This is like a SQL SELECT * FROM core_contactmessage
all_messages = ContactMessage.objects.all().order_by('-created_at')

print(f"Found {all_messages.count()} total messages in the database:\n")

for msg in all_messages[:5]:  # Show top 5
    print(f"[ID: {msg.id}] {msg.name} ({msg.email}): {msg.message}")

print("----------------------------------------------------------------")
