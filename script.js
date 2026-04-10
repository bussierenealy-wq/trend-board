// TrendBoard v2.0 - Intelligence Core
const platformConfig = {
    bilibili: { name: 'Bilibili 热搜', icon: '📺', active: true },
    xhs: { name: '小红书精选', icon: '🌸', active: true },
    weibo: { name: '微博热搜', icon: '🔥', active: true },
    xueqiu: { name: '雪球财经', icon: '📈', active: true },
    '36kr': { name: '36氪热门', icon: '💡', active: true }
};

document.addEventListener('DOMContentLoaded', () => {
    initUI();
    fetchTrends();
});

function initUI() {
    const toggleContainer = document.getElementById('source-toggles');
    toggleContainer.innerHTML = '';

    Object.keys(platformConfig).forEach(id => {
        const config = platformConfig[id];
        const item = document.createElement('div');
        item.className = `toggle-item ${config.active ? 'active' : ''}`;
        item.setAttribute('data-id', id);
        item.innerHTML = `
            <div class="toggle-info">
                <i class="toggle-icon">${config.icon}</i>
                <span>${config.name}</span>
            </div>
            <div class="switch"></div>
        `;
        
        item.onclick = () => {
            config.active = !config.active;
            item.classList.toggle('active');
            renderActivePlatforms();
        };
        
        toggleContainer.appendChild(item);
    });

    document.getElementById('sync-btn').onclick = syncData;
    
    // Grid controls
    document.querySelectorAll('.view-tab').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.view-tab').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const cols = btn.dataset.grid;
            document.getElementById('trends-board').style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        };
    });
}

async function fetchTrends() {
    try {
        const res = await fetch('/api/trends');
        const data = await res.json();
        window.cachedData = data;
        renderActivePlatforms();
        document.getElementById('last-update').innerText = `更新于 ${new Date().toLocaleTimeString()}`;
    } catch (e) {
        console.error("Backend offline", e);
    }
}

async function syncData() {
    const btn = document.getElementById('sync-btn');
    btn.disabled = true;
    btn.innerHTML = '同步中...';
    try {
        const res = await fetch('/api/sync', { method: 'POST' });
        const data = await res.json();
        window.cachedData = data;
        renderActivePlatforms();
        document.getElementById('last-update').innerText = `更新于 ${new Date().toLocaleTimeString()}`;
    } catch (e) {
        alert("同步异常，请检查后端状态");
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="sync-icon">🔄</span> 立即同步';
    }
}

function renderActivePlatforms() {
    const board = document.getElementById('trends-board');
    board.innerHTML = '';
    const data = window.cachedData || {};

    Object.keys(platformConfig).forEach(id => {
        if (platformConfig[id].active && data[id]) {
            const channelCard = createChannelCard(id, data[id]);
            board.appendChild(channelCard);
        }
    });
}

function createChannelCard(id, items) {
    const config = platformConfig[id];
    const card = document.createElement('section');
    card.className = 'channel-card';
    
    const header = `
        <div class="card-header">
            <h3>${config.icon} ${config.name}</h3>
            <span class="count-tag">${items.length}</span>
        </div>
    `;
    
    let listHtml = '<div class="feed-list">';
    items.forEach(item => {
        listHtml += `
            <a href="${item.url}" target="_blank" class="trend-item">
                <div class="trend-title">${item.title}</div>
                <div class="trend-meta">
                    <span class="trend-desc">${item.desc}</span>
                    <span class="hot-tag">${item.hot}</span>
                </div>
            </a>
        `;
    });
    listHtml += '</div>';
    
    card.innerHTML = header + listHtml;
    return card;
}
