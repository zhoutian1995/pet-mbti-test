#!/usr/bin/env node
/**
 * willeai.cn 自动截图脚本
 * 使用 Playwright 截取指定页面
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// 截图配置
const PAGES = [
    {
        url: 'https://www.willeai.cn/for-ai.html',
        name: 'for-ai',
        desc: 'For AI 页面 - 状态栏特写',
        selector: 'footer'
    },
    {
        url: 'https://www.willeai.cn/',
        name: 'index',
        desc: '首页 - 双卡片布局',
        selector: 'main'
    },
    {
        url: 'https://www.willeai.cn/for-humans.html',
        name: 'for-humans',
        desc: 'For Humans - GrowthCompass + 占位符',
        selector: 'main'
    },
    {
        url: 'https://www.willeai.cn/article-macmini.html',
        name: 'article-macmini',
        desc: '文章页 - YAML + Copy 按钮',
        selector: '#view-machine'
    },
    {
        url: 'https://www.willeai.cn/about.html',
        name: 'about',
        desc: '关于页 - Connections 模块',
        selector: 'main'
    }
];

const OUTPUT_DIR = path.join(process.env.HOME, 'Desktop', 'willeai-screenshots');

async function main() {
    console.log('📸 开始截图 willeai.cn 页面...\n');
    
    // 创建输出目录
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
        console.log(`✅ 创建输出目录：${OUTPUT_DIR}\n`);
    }
    
    // 启动浏览器
    const browser = await chromium.launch({
        headless: true,
        args: [
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--no-sandbox'
        ]
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        deviceScaleFactor: 2  // Retina 高清
    });
    
    const results = [];
    
    for (const page of PAGES) {
        try {
            console.log(`📷 截图：${page.name}`);
            console.log(`   URL: ${page.url}`);
            console.log(`   描述：${page.desc}`);
            
            const pageContext = await context.newPage();
            await pageContext.goto(page.url, { 
                waitUntil: 'networkidle',
                timeout: 30000 
            });
            
            // 等待页面加载
            await pageContext.waitForTimeout(2000);
            
            // 截图
            const screenshotPath = path.join(OUTPUT_DIR, `${page.name}.png`);
            
            if (page.selector) {
                // 截取特定元素
                const element = await pageContext.$(page.selector);
                if (element) {
                    await element.screenshot({ 
                        path: screenshotPath,
                        type: 'png'
                    });
                    console.log(`   ✅ 元素截图完成：${screenshotPath}`);
                } else {
                    console.log(`   ⚠️ 未找到选择器 ${page.selector}，截取全屏`);
                    await pageContext.screenshot({ 
                        path: screenshotPath,
                        type: 'png',
                        fullPage: true
                    });
                }
            } else {
                await pageContext.screenshot({ 
                    path: screenshotPath,
                    type: 'png',
                    fullPage: true
                });
            }
            
            results.push({
                name: page.name,
                path: screenshotPath,
                success: true
            });
            
            await pageContext.close();
            console.log('');
            
        } catch (error) {
            console.log(`   ❌ 失败：${error.message}\n`);
            results.push({
                name: page.name,
                error: error.message,
                success: false
            });
        }
    }
    
    await browser.close();
    
    // 输出结果
    console.log('═══════════════════════════════════════');
    console.log('📊 截图结果汇总');
    console.log('═══════════════════════════════════════\n');
    
    const successCount = results.filter(r => r.success).length;
    const failCount = results.filter(r => !r.success).length;
    
    console.log(`✅ 成功：${successCount}/${results.length}`);
    console.log(`❌ 失败：${failCount}/${results.length}\n`);
    
    console.log('输出文件:');
    results.forEach(r => {
        if (r.success) {
            console.log(`  📁 ${r.path}`);
        } else {
            console.log(`  ❌ ${r.name}: ${r.error}`);
        }
    });
    
    console.log('\n✨ 完成！\n');
}

main().catch(console.error);
