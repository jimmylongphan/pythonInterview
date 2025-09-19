#!/usr/bin/env python3

import requests
import threading
import time
import json

def send_message(source, destination, message, thread_id):
    """Send a message from a specific thread"""
    url = "http://localhost:8080/new_message"
    data = {
        "source_user_id": source,
        "destination_user_id": destination,
        "message": f"[Thread {thread_id}] {message}"
    }
    
    start_time = time.time()
    try:
        response = requests.post(url, json=data, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            duration = end_time - start_time
            print(f"✅ Thread {thread_id}: Sent message in {duration:.3f}s")
            print(f"   Chat history length: {len(result.get('chat_history', []))}")
            return result
        else:
            print(f"❌ Thread {thread_id}: Error {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Thread {thread_id}: Exception - {e}")
        return None

def main():
    print("🚀 Simple Concurrent Client Test")
    print("=" * 40)
    
    # Test data
    users = ["user1", "user2", "user3", "user4"]
    messages = ["Hello!", "How are you?", "What's up?", "Nice day!", "See you later!"]
    
    # Create threads
    threads = []
    num_threads = 5
    
    print(f"Starting {num_threads} concurrent threads...")
    start_time = time.time()
    
    for i in range(num_threads):
        source = users[i % len(users)]
        destination = users[(i + 1) % len(users)]
        message = messages[i % len(messages)]
        
        thread = threading.Thread(
            target=send_message,
            args=(source, destination, message, i+1)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    print("=" * 40)
    print(f"✅ All {num_threads} threads completed in {total_duration:.3f} seconds")
    print(f"   Average per thread: {total_duration/num_threads:.3f} seconds")

if __name__ == "__main__":
    main()
