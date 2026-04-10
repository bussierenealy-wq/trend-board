function updateTime() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    document.getElementById('date-display').innerText = new Date().toLocaleDateString('zh-CN', options) + " [实时流]";
}

function createCard(item, isNew = false) {
    const card = document.createElement('div');
    card.className = `card ${isNew ? 'new-entry' : ''}`;
    
    if (item.url) {
        card.style.cursor = 'pointer';
        card.onclick = () => window.open(item.url, '_blank');
        card.title = "点击查看详情";
    }

    card.innerHTML = `
        <div class="card-meta">
            <span>风向标</span>
            <span class="card-hotness">${item.hot}</span>
        </div>
        <h3 class="card-title">${item.title}</h3>
        <p class="card-desc">${item.desc}</p>
    `;
    return card;
}

function renderPlat(platId, data) {
    const container = document.getElementById(`feed-${platId}`);
    // No more max constraint, just map the backend payload limits
    container.innerHTML = '';
    data.forEach(item => {
        container.appendChild(createCard(item));
    });
}

async function fetchRealData() {
    try {
        const response = await fetch('/api/trends');
        const data = await response.json();
        
        if(data.bilibili.length > 0) renderPlat('bilibili', data.bilibili);
        if(data.xhs.length > 0) renderPlat('xhs', data.xhs);
        if(data.xueqiu.length > 0) renderPlat('xueqiu', data.xueqiu);
        if(data.weibo && data.weibo.length > 0) renderPlat('weibo', data.weibo);
        
    } catch (e) {
        console.error("Failed to fetch data, is backend running?", e);
    }
}

function init() {
    updateTime();
    setInterval(updateTime, 1000);
    
    // Initial fetch
    fetchRealData();
    
    // Sync Button mapped to trigger Backend Force Sync
    document.getElementById('force-sync').addEventListener('click', async (e) => {
        const btn = e.target;
        if(btn.innerText.includes('同步中')) return;
        
        btn.innerText = "正在同步...";
        const originalBg = btn.style.backgroundColor;
        btn.style.backgroundColor = 'var(--text-gray)';
        
        try {
            const resp = await fetch('/api/sync', { method: 'POST' });
            const data = await resp.json();
            if(data.bilibili.length > 0) renderPlat('bilibili', data.bilibili);
            if(data.xhs.length > 0) renderPlat('xhs', data.xhs);
            if(data.xueqiu.length > 0) renderPlat('xueqiu', data.xueqiu);
            if(data.weibo && data.weibo.length > 0) renderPlat('weibo', data.weibo);
        } catch(e) {
            console.error("Sync Error", e);
        }
        
        btn.innerText = "立即同步";
        btn.style.backgroundColor = originalBg;
    });
}

document.addEventListener('DOMContentLoaded', init);
