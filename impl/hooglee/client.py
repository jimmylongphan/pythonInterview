#!/usr/bin/env python3

import requests
import threading
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

class ChatClient:
    def __init__(self, server_url="http://localhost:8080"):
        self.server_url = server_url
        self.session = requests.Session()
    
    def send_message(self, source_user_id, destination_user_id, message):
        """Send a single message to the server"""
        url = f"{self.server_url}/new_message"
        data = {
            "source_user_id": source_user_id,
            "destination_user_id": destination_user_id,
            "message": message
        }
        
        try:
            response = self.session.post(url, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Message sent from {source_user_id} to {destination_user_id}: '{message}'")
                print(f"   Response: {len(result.get('chat_history', []))} messages in chat")
                return result
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Exception sending message: {e}")
            return None
    
    def delete_message(self, source_user_id, destination_user_id, message_id):
        """Delete a message from the server"""
        url = f"{self.server_url}/delete_message"
        data = {
            "source_user_id": source_user_id,
            "destination_user_id": destination_user_id,
            "message_id": message_id
        }
        
        try:
            response = self.session.delete(url, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                print(f"🗑️  Message {message_id} deleted: {result.get('status')}")
                return result
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Exception deleting message: {e}")
            return None
    
    def get_chat_history(self, source_user_id, destination_user_id):
        """Get chat history by sending a dummy message and extracting history"""
        # Send a dummy message to get the current chat history
        dummy_result = self.send_message(source_user_id, destination_user_id, "DUMMY_GET_HISTORY")
        if dummy_result and 'chat_history' in dummy_result:
            # Remove the dummy message we just added
            chat_history = dummy_result['chat_history']
            if chat_history and chat_history[-1].get('message') == "DUMMY_GET_HISTORY":
                chat_history.pop()
            return chat_history
        return []
    
    def generate_expected_chat_history(self, sent_messages, deleted_message_ids=None):
        """
        Generate expected chat history based on sent messages and deletions
        
        Args:
            sent_messages: List of messages that were sent
            deleted_message_ids: Set of message IDs that were deleted
        """
        if deleted_message_ids is None:
            deleted_message_ids = set()
        
        # Group messages by chat pairs
        chat_pairs = {}
        for msg in sent_messages:
            source = msg['source_user_id']
            dest = msg['destination_user_id']
            # Create consistent chat ID (sorted)
            chat_id = tuple(sorted([source, dest]))
            if chat_id not in chat_pairs:
                chat_pairs[chat_id] = []
            chat_pairs[chat_id].append(msg)
        
        # Generate expected history for each chat
        expected_history = {}
        for chat_id, messages in chat_pairs.items():
            # Filter out deleted messages
            remaining_messages = []
            for msg in messages:
                # We need to track which messages were actually sent and got IDs
                # For now, we'll assume all messages were sent successfully
                remaining_messages.append(msg)
            
            # Sort by timestamp (if available) or by order sent
            remaining_messages.sort(key=lambda x: x.get('timestamp', 0))
            expected_history[chat_id] = remaining_messages
        
        return expected_history
    
    def assert_chat_history_integrity(self, sent_messages, message_results, deleted_message_ids=None):
        """
        Assert that chat history is consistent after concurrent operations
        
        Args:
            sent_messages: List of messages that were sent to the server
            message_results: List of results from concurrent message sending
            deleted_message_ids: Set of message IDs that were deleted
        """
        print(f"\n🔍 Asserting chat history integrity...")
        print(f"   Sent messages: {len(sent_messages)}")
        print(f"   Message results: {len(message_results)}")
        print(f"   Deleted messages: {len(deleted_message_ids) if deleted_message_ids else 0}")
        
        # Generate expected chat history
        expected_history = self.generate_expected_chat_history(sent_messages, deleted_message_ids)
        
        # Extract actual chat history from message results
        actual_history_by_chat = {}
        for result in message_results:
            if result and 'chat_history' in result:
                # Get the last message to determine the chat pair
                if result['chat_history']:
                    last_msg = result['chat_history'][-1]
                    source = last_msg.get('source_user_id')
                    dest = last_msg.get('destination_user_id')
                    if source and dest:
                        chat_id = tuple(sorted([source, dest]))
                        # Use the most recent chat history for this chat
                        actual_history_by_chat[chat_id] = result['chat_history']
        
        all_assertions_passed = True
        
        for chat_id, expected_chat_messages in expected_history.items():
            source, dest = chat_id
            print(f"\n   Checking chat: {source} ↔ {dest}")
            
            # Get actual chat history from results
            actual_history = actual_history_by_chat.get(chat_id, [])
            actual_count = len(actual_history)
            expected_count = len(expected_chat_messages)
            
            print(f"   Expected: {expected_count} messages")
            print(f"   Actual: {actual_count} messages")
            
            # Check exact message count
            if actual_count != expected_count:
                print(f"   ❌ FAIL: Message count mismatch (expected {expected_count}, got {actual_count})")
                all_assertions_passed = False
            else:
                print(f"   ✅ PASS: Message count matches exactly")
            
            # Check for duplicate message IDs
            actual_ids = [msg.get('id') for msg in actual_history if msg.get('id')]
            unique_ids = set(actual_ids)
            if len(actual_ids) != len(unique_ids):
                print(f"   ❌ FAIL: Duplicate message IDs found")
                all_assertions_passed = False
            else:
                print(f"   ✅ PASS: No duplicate message IDs")
            
            # Check timestamp ordering (should be ascending)
            timestamps = [msg.get('timestamp', 0) for msg in actual_history if msg.get('timestamp')]
            if timestamps != sorted(timestamps):
                print(f"   ❌ FAIL: Messages not in chronological order")
                all_assertions_passed = False
            else:
                print(f"   ✅ PASS: Messages in chronological order")
            
            # Check message structure and content
            for i, msg in enumerate(actual_history):
                required_fields = ['id', 'source_user_id', 'timestamp', 'message']
                missing_fields = [field for field in required_fields if field not in msg]
                if missing_fields:
                    print(f"   ❌ FAIL: Message {i} missing fields: {missing_fields}")
                    all_assertions_passed = False
                else:
                    print(f"   ✅ PASS: Message {i} has all required fields")
            
            # Check that deleted messages are not present
            if deleted_message_ids:
                actual_ids_set = set(actual_ids)
                deleted_present = actual_ids_set.intersection(deleted_message_ids)
                if deleted_present:
                    print(f"   ❌ FAIL: Deleted messages still present: {deleted_present}")
                    all_assertions_passed = False
                else:
                    print(f"   ✅ PASS: No deleted messages found in chat")
            
            # Check that actual messages match expected messages (excluding server-generated fields)
            if actual_count == expected_count:
                print(f"   🔍 Verifying message content matches...")
                for i, (actual_msg, expected_msg) in enumerate(zip(actual_history, expected_chat_messages)):
                    # Compare message content (excluding server-generated id and timestamp)
                    if (actual_msg.get('source_user_id') == expected_msg.get('source_user_id') and
                        actual_msg.get('message') == expected_msg.get('message')):
                        print(f"   ✅ PASS: Message {i} content matches")
                    else:
                        print(f"   ❌ FAIL: Message {i} content mismatch")
                        print(f"      Expected: {expected_msg}")
                        print(f"      Actual: {actual_msg}")
                        all_assertions_passed = False
        
        print(f"\n{'='*50}")
        if all_assertions_passed:
            print("🎉 ALL ASSERTIONS PASSED - Chat history integrity verified!")
        else:
            print("❌ SOME ASSERTIONS FAILED - Chat history integrity issues detected!")
        
        return all_assertions_passed

def send_concurrent_messages(client, num_messages=10, num_threads=5):
    """Send multiple messages concurrently using ThreadPoolExecutor"""
    print(f"🚀 Starting concurrent message sending...")
    print(f"   Messages: {num_messages}")
    print(f"   Threads: {num_threads}")
    print("-" * 50)
    
    # Generate test data
    users = ["alice", "bob", "charlie", "diana", "eve"]
    messages = [
        "Hello there!",
        "How are you doing?",
        "What's up?",
        "Nice to meet you!",
        "How's your day going?",
        "Any plans for today?",
        "Hope you're having a great time!",
        "Thanks for the message!",
        "See you later!",
        "Have a wonderful day!"
    ]
    
    # Store expected messages for assertion
    expected_messages = []
    
    def send_random_message():
        source = random.choice(users)
        destination = random.choice([u for u in users if u != source])
        message = random.choice(messages)
        
        # Store expected message data
        expected_msg = {
            'source_user_id': source,
            'destination_user_id': destination,
            'message': message
        }
        expected_messages.append(expected_msg)
        
        return client.send_message(source, destination, message)
    
    start_time = time.time()
    
    # Use ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all tasks
        futures = [executor.submit(send_random_message) for _ in range(num_messages)]
        
        # Collect results as they complete
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("-" * 50)
    print(f"✅ Completed {num_messages} concurrent messages in {duration:.2f} seconds")
    print(f"   Average: {duration/num_messages:.3f} seconds per message")
    print(f"   Throughput: {num_messages/duration:.1f} messages/second")
    
    # Assert chat history integrity
    client.assert_chat_history_integrity(expected_messages, results)
    
    return results, expected_messages

def test_concurrent_deletions(client, message_results):
    """Test concurrent message deletions"""
    print(f"\n🗑️  Testing concurrent message deletions...")
    
    # Extract message IDs from results
    message_ids = []
    for result in message_results:
        if result and 'chat_history' in result:
            for msg in result['chat_history']:
                if 'id' in msg:
                    message_ids.append({
                        'id': msg['id'],
                        'source': msg['source_user_id'],
                        'destination': 'bob'  # Default destination for deletion test
                    })
    
    if not message_ids:
        print("❌ No message IDs found for deletion test")
        return set()
    
    # Test deleting first few messages concurrently
    test_messages = message_ids[:3]
    deleted_message_ids = set()
    
    def delete_message_task(msg_data):
        result = client.delete_message(msg_data['source'], msg_data['destination'], msg_data['id'])
        if result and result.get('status') == 'success':
            deleted_message_ids.add(msg_data['id'])
        return result
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(delete_message_task, msg) for msg in test_messages]
        
        for future in as_completed(futures):
            result = future.result()
    
    return deleted_message_ids

def main():
    print("🎯 Chat Server Concurrent Client")
    print("=" * 50)
    
    # Create client
    client = ChatClient()
    
    # Test server connection
    print("🔍 Testing server connection...")
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        print("✅ Server is running!")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running on port 8080")
        return
    
    # Send concurrent messages
    results, expected_messages = send_concurrent_messages(client, num_messages=15, num_threads=8)
    
    # Test concurrent deletions
    deleted_message_ids = test_concurrent_deletions(client, results)
    
    # Final integrity check after deletions
    print(f"\n🔍 Final integrity check after deletions...")
    client.assert_chat_history_integrity(expected_messages, results, deleted_message_ids)
    
    print("\n🎉 Concurrent testing completed!")

if __name__ == "__main__":
    main()
