/**
 * Swagger UI 中文汉化脚本
 * 将 Swagger 界面中的英文标签替换为中文，方便国内面试官和导师阅读
 */
(function () {
    // 等待 Swagger UI 渲染完成后执行
    function translate() {
        // ── 翻译映射表 ──
        const map = {
            // 顶部操作栏
            "Explore": "接口导航",
            "Search": "搜索接口...",

            // 认证
            "Authorize": "🔐 认证",
            "Available authorizations": "可用认证方式",
            "Close": "关闭",

            // 接口操作按钮
            "Try it out": "▶ 在线调试",
            "Cancel": "取消",
            "Execute": "▶ 执行请求",
            "Clear": "清除",

            // 请求 / 响应区域
            "Parameters": "请求参数",
            "No parameters": "无需参数",
            "Request body": "请求体",
            "Example Value": "示例值",
            "Schema": "数据结构",

            // 响应
            "Responses": "响应结果",
            "Response": "响应",
            "Server response": "服务器返回",
            "Code": "状态码",
            "Details": "详情",
            "Description": "说明",

            // 底部
            "Download": "下载",
            "Select language": "选择语言",

            // 其他
            "Send empty value": "发送空值",
            "application/json": "JSON 格式",
            "string": "字符串",
            "integer": "整数",
            "number": "数字",
            "boolean": "布尔值",
            "object": "对象",
            "array": "数组",
            "null": "空值",

            // curl 示例
            "Request URL": "请求地址",
            "Curl": "Curl 命令",

            // 响应码
            "Undocumented": "未文档化",
            "default": "默认",
        };

        // ── 遍历所有文本节点进行替换 ──
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const nodes = [];
        while (walker.nextNode()) {
            nodes.push(walker.currentNode);
        }

        nodes.forEach(function (node) {
            let text = node.textContent.trim();
            if (map[text]) {
                node.textContent = map[text];
            } else if (map[node.textContent]) {
                node.textContent = map[node.textContent];
            }
        });

        // ── 修改 aria-label 和 placeholder ──
        document.querySelectorAll('[placeholder]').forEach(function (el) {
            if (el.placeholder === 'Search') {
                el.placeholder = '搜索接口...';
            }
        });

        document.querySelectorAll('input[title]').forEach(function (el) {
            if (el.title === 'Search') {
                el.title = '搜索接口';
            }
        });

        // ── 修改 "Try it out" 按钮文字（它可能不在文本节点中） ──
        document.querySelectorAll('.try-out__btn').forEach(function (btn) {
            if (btn.textContent.trim() === 'Try it out') {
                btn.textContent = '▶ 在线调试';
            }
        });

        // ── 修改 "Cancel" 按钮 ──
        document.querySelectorAll('.btn.cancel').forEach(function (btn) {
            if (btn.textContent.trim() === 'Cancel') {
                btn.textContent = '取消';
            }
        });

        // ── 修改 "Execute" 按钮 ──
        document.querySelectorAll('.execute-wrapper .btn').forEach(function (btn) {
            if (btn.textContent.trim() === 'Execute') {
                btn.textContent = '▶ 执行请求';
            }
        });

        // ── 修改 "Clear" 按钮 ──
        document.querySelectorAll('.btn.clear').forEach(function (btn) {
            if (btn.textContent.trim() === 'Clear') {
                btn.textContent = '清除';
            }
        });
    }

    // ── DOM 变化时持续翻译（Swagger 动态加载内容） ──
    let translating = false;
    let debounceTimer = null;

    function safeTranslate() {
        if (translating) return;
        translating = true;
        observer.disconnect();      // 先断开监听，避免自己触发自己
        translate();
        observer.observe(document.body, { childList: true, subtree: true, characterData: true });
        translating = false;
    }

    var observer = new MutationObserver(function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(safeTranslate, 100);  // 100ms 防抖
    });

    function watch() {
        translate();
        observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    }

    // 页面加载完成后启动
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', watch);
    } else {
        watch();
    }
})();
