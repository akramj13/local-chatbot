#!/usr/bin/env python3
"""Simple test script to validate the chatbot API functionality."""

import asyncio
import json
import httpx
import time
from typing import Dict, Any


class ChatbotAPITester:
    """Test class for validating chatbot API functionality."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the tester with base URL."""
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()
    
    async def test_health_check(self) -> bool:
        """Test the health check endpoint."""
        try:
            print("🔍 Testing health check...")
            response = await self.client.get(f"{self.base_url}/api/v1/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                print(f"   Model: {data['model']}")
                print(f"   Version: {data['version']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    async def test_models_endpoint(self) -> bool:
        """Test the models listing endpoint."""
        try:
            print("\n🔍 Testing models endpoint...")
            response = await self.client.get(f"{self.base_url}/api/v1/models")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Models endpoint working")
                print(f"   Available models: {data['models']}")
                print(f"   Default model: {data['default_model']}")
                return True
            else:
                print(f"❌ Models endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Models endpoint error: {e}")
            return False
    
    async def test_chat_complete(self) -> bool:
        """Test the complete chat endpoint."""
        try:
            print("\n🔍 Testing complete chat...")
            payload = {
                "message": "Hello! Please respond with 'Test successful' if you can understand this.",
                "temperature": 0.7
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/chat",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Complete chat working")
                print(f"   Response: {data['message'][:100]}...")
                print(f"   Model: {data['model']}")
                print(f"   Conversation ID: {data['conversation_id']}")
                return True
            else:
                print(f"❌ Complete chat failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Complete chat error: {e}")
            return False
    
    async def test_chat_streaming(self) -> bool:
        """Test the streaming chat endpoint."""
        try:
            print("\n🔍 Testing streaming chat...")
            payload = {
                "message": "Count from 1 to 3, each number on a new line.",
                "stream": True,
                "temperature": 0.3
            }
            
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/v1/chat/stream",
                json=payload
            ) as response:
                
                if response.status_code != 200:
                    print(f"❌ Streaming chat failed: {response.status_code}")
                    return False
                
                chunks_received = 0
                content_received = ""
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix
                        if data_str == "[DONE]":
                            break
                        
                        try:
                            chunk_data = json.loads(data_str)
                            content_received += chunk_data.get("content", "")
                            chunks_received += 1
                            
                            if chunk_data.get("is_complete", False):
                                break
                                
                        except json.JSONDecodeError:
                            continue
                
                if chunks_received > 0:
                    print(f"✅ Streaming chat working")
                    print(f"   Chunks received: {chunks_received}")
                    print(f"   Content sample: {content_received[:100]}...")
                    return True
                else:
                    print(f"❌ No chunks received in streaming")
                    return False
                    
        except Exception as e:
            print(f"❌ Streaming chat error: {e}")
            return False
    
    async def test_conversation_management(self) -> bool:
        """Test conversation history management."""
        try:
            print("\n🔍 Testing conversation management...")
            
            # Start a conversation
            payload = {
                "message": "Remember this number: 42",
                "temperature": 0.5
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/chat",
                json=payload
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to start conversation: {response.status_code}")
                return False
            
            conversation_id = response.json()["conversation_id"]
            
            # Continue the conversation
            payload2 = {
                "message": "What number did I ask you to remember?",
                "temperature": 0.3
            }
            
            response2 = await self.client.post(
                f"{self.base_url}/api/v1/chat?conversation_id={conversation_id}",
                json=payload2
            )
            
            if response2.status_code != 200:
                print(f"❌ Failed to continue conversation: {response2.status_code}")
                return False
            
            # Get conversation history
            history_response = await self.client.get(
                f"{self.base_url}/api/v1/conversation/{conversation_id}"
            )
            
            if history_response.status_code != 200:
                print(f"❌ Failed to get conversation history: {history_response.status_code}")
                return False
            
            history_data = history_response.json()
            message_count = history_data["message_count"]
            
            print(f"✅ Conversation management working")
            print(f"   Conversation ID: {conversation_id}")
            print(f"   Messages in history: {message_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Conversation management error: {e}")
            return False
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests and return results."""
        print("🚀 Starting Chatbot API Tests\n")
        
        results = {}
        
        # Test health check first
        results["health"] = await self.test_health_check()
        
        if not results["health"]:
            print("\n❌ Health check failed - skipping other tests")
            return results
        
        # Wait a moment for the service to be fully ready
        await asyncio.sleep(2)
        
        # Run other tests
        results["models"] = await self.test_models_endpoint()
        results["chat_complete"] = await self.test_chat_complete()
        results["chat_streaming"] = await self.test_chat_streaming()
        results["conversation"] = await self.test_conversation_management()
        
        # Summary
        print(f"\n📊 Test Results Summary:")
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        passed_tests = sum(results.values())
        total_tests = len(results)
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
        
        return results


async def main():
    """Main test function."""
    print("Chatbot API Test Suite")
    print("=" * 50)
    
    # Wait for service to be ready
    print("⏳ Waiting for service to be ready...")
    await asyncio.sleep(5)
    
    async with ChatbotAPITester() as tester:
        results = await tester.run_all_tests()
        
        # Exit with appropriate code
        if all(results.values()):
            print("\n🎉 All tests passed!")
            return 0
        else:
            print("\n💥 Some tests failed!")
            return 1


if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 