// i18n.js - 语言切换工具

// 获取当前语言（默认中文）
function getLanguage() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lang') || 'zh';
}

// 切换语言
function switchLanguage(lang) {
    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
}

// 获取语言按钮文本
function getLanguageButtonLabel() {
    const lang = getLanguage();
    return lang === 'zh' ? 'EN' : '中文';
}

// 获取切换目标语言
function getTargetLanguage() {
    const lang = getLanguage();
    return lang === 'zh' ? 'en' : 'zh';
}

// 获取语言切换按钮 HTML
function getLanguageSwitchButton() {
    const lang = getLanguage();
    const label = getLanguageButtonLabel();
    const target = getTargetLanguage();

    return `
        <button onclick="switchLanguage('${target}')" class="text-xs text-neutral-500 hover:text-white border border-neutral-700 px-3 py-1 rounded-full hover:border-neutral-500 transition-all">
            ${label}
        </button>
    `;
}

// 页面加载完成后添加语言切换按钮
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('header nav') || document.querySelector('header');
    if (nav) {
        const buttonContainer = document.createElement('div');
        buttonContainer.innerHTML = getLanguageSwitchButton();
        nav.appendChild(buttonContainer);
    }
});
