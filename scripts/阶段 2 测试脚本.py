#!/usr/bin/env python3
"""
微信公众号 API 测试脚本 (阶段 2)
等待 IP 白名单配置完成后运行
"""
import requests
import json
from pathlib import Path

# 微信公众号配置
APP_ID = "wx8a9b4f72b05ba667"
APP_SECRET = "958b6facdc92bc04362136f501b0a71f"

class WeChatAPITester:
    def __init__(self):
        self.access_token = None
    
    def get_access_token(self):
        """获取 access_token"""
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": APP_ID,
            "secret": APP_SECRET
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        if 'access_token' in data:
            self.access_token = data['access_token']
            print(f"✅ access_token 获取成功")
            return True
        else:
            print(f"❌ access_token 获取失败：{data}")
            return False
    
    def test_draft_list(self):
        """测试获取草稿列表"""
        url = "https://api.weixin.qq.com/cgi-bin/draft/batchget"
        params = {"access_token": self.access_token}
        payload = {"offset": 0, "count": 5}
        
        resp = requests.post(url, params=params, json=payload, timeout=10)
        data = resp.json()
        
        if 'item' in data:
            print(f"✅ 草稿列表获取成功，共 {len(data['item'])} 篇")
            for i, item in enumerate(data['item'][:5]):
                title = item.get('article_info', {}).get('title', '未知')
                update_time = item.get('article_info', {}).get('update_time', 0)
                print(f"   {i+1}. {title} (更新时间：{update_time})")
            return True
        else:
            print(f"❌ 草稿列表获取失败：{data}")
            return False
    
    def test_create_draft(self):
        """测试创建草稿"""
        url = "https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {"access_token": self.access_token}
        
        payload = {
            "articles": [{
                "title": "测试文章 - 阶段 2 API 测试",
                "author": "Bob",
                "digest": "这是自动测试创建的草稿",
                "content": "<p>这是测试内容，证明 API 连通正常。</p>",
                "thumb_media_id": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }]
        }
        
        resp = requests.post(url, params=params, json=payload, timeout=30)
        data = resp.json()
        
        if 'media_id' in data:
            print(f"✅ 草稿创建成功，media_id: {data['media_id']}")
            return data['media_id']
        else:
            print(f"❌ 草稿创建失败：{data}")
            return None
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 50)
        print("微信公众号 API 阶段 2 测试")
        print("=" * 50)
        
        # 测试 1: 获取 access_token
        print("\n📡 测试 1: 获取 access_token...")
        if not self.get_access_token():
            print("\n❌ 测试失败：无法获取 access_token")
            return False
        
        # 测试 2: 获取草稿列表
        print("\n📡 测试 2: 获取草稿列表...")
        self.test_draft_list()
        
        # 测试 3: 创建测试草稿
        print("\n📡 测试 3: 创建测试草稿...")
        media_id = self.test_create_draft()
        
        print("\n" + "=" * 50)
        print("✅ 阶段 2 测试完成")
        print("=" * 50)
        
        return True

if __name__ == '__main__':
    tester = WeChatAPITester()
    tester.run_all_tests()
