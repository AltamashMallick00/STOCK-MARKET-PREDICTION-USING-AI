const API_BASE = ""; // Relative path since frontend is served by backend
let chart = null;
let longTermChart = null;

const elements = {
    stockSelect: document.getElementById('stockSelect'),
    predictBtn: document.getElementById('predictBtn'),
    loader: document.getElementById('loader'),
    statsGrid: document.getElementById('statsGrid'),
    welcomeMsg: document.getElementById('welcomeMsg'),
    lrVal: document.getElementById('lrVal'),
    lstmVal: document.getElementById('lstmVal'),
    agVal: document.getElementById('agVal'),
    canvas: document.getElementById('predictionChart').getContext('2d'),
    longCanvas: document.getElementById('longTermChart').getContext('2d'),
    themeToggle: document.getElementById('themeToggle'),
    tabBtns: document.querySelectorAll('.tab-btn')
};

// Theme Toggle
elements.themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
});

// Load saved theme
if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light-theme');
}

// Tab Switching
elements.tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        elements.tabBtns.forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(`${btn.dataset.tab}Tab`).classList.add('active');
    });
});

// Fetch available stocks on load
async function init() {
    try {
        const res = await fetch(`${API_BASE}/stocks`);
        const data = await res.json();
        
        data.stocks.forEach(stock => {
            const option = document.createElement('option');
            option.value = stock;
            option.textContent = stock;
            elements.stockSelect.appendChild(option);
        });
    } catch (err) {
        console.error("Failed to load stocks:", err);
    }
}

async function runPrediction() {
    const symbol = elements.stockSelect.value;
    if (!symbol) return alert("Please select a stock first");

    elements.loader.style.display = 'flex';
    
    try {
        const res = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol })
        });
        
        const data = await res.json();
        updateUI(data);
    } catch (err) {
        console.error("Prediction failed:", err);
        alert("Error connecting to backend");
    } finally {
        elements.loader.style.display = 'none';
    }
}

function updateUI(data) {
    elements.welcomeMsg.style.display = 'none';
    elements.statsGrid.style.display = 'grid';
    
    elements.lrVal.textContent = `$${data.predictions.linear_regression.toFixed(2)}`;
    elements.lstmVal.textContent = `$${data.predictions.lstm.toFixed(2)}`;
    elements.agVal.textContent = `$${data.predictions.antigravity.toFixed(2)}`;
    
    renderChart(data);
    renderLongTermChart(data.long_term);
}

function renderChart(data) {
    if (chart) chart.destroy();
    
    const historyDates = data.history.map(h => h.Date.split(' ')[0]);
    const historyPrices = data.history.map(h => h.Close);
    
    const lastDate = new Date(historyDates[historyDates.length - 1]);
    const nextDate = new Date(lastDate);
    nextDate.setDate(nextDate.getDate() + 1);
    const nextDateStr = nextDate.toISOString().split('T')[0];
    
    const labels = [...historyDates, nextDateStr];
    
    chart = new Chart(elements.canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Historical Price',
                    data: historyPrices,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Linear Regression',
                    data: [...Array(historyPrices.length).fill(null), data.predictions.linear_regression],
                    borderColor: '#94a3b8',
                    borderDash: [5, 5],
                    pointRadius: 6
                },
                {
                    label: 'LSTM Prediction',
                    data: [...Array(historyPrices.length).fill(null), data.predictions.lstm],
                    borderColor: '#22c55e',
                    borderDash: [5, 5],
                    pointRadius: 6
                },
                {
                    label: 'Antigravity Prediction',
                    data: [...Array(historyPrices.length).fill(null), data.predictions.antigravity],
                    borderColor: '#a855f7',
                    borderWidth: 3,
                    pointRadius: 8,
                    pointBackgroundColor: '#a855f7'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: 'inherit' } }
            },
            scales: {
                y: { grid: { color: 'rgba(128, 128, 128, 0.1)' }, ticks: { color: 'inherit' } },
                x: { grid: { display: false }, ticks: { color: 'inherit' } }
            }
        }
    });
}

function renderLongTermChart(longTermData) {
    if (longTermChart) longTermChart.destroy();
    
    const labels = longTermData.map(d => d.year);
    const prices = longTermData.map(d => d.price);
    
    longTermChart = new Chart(elements.longCanvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Projected Year-End Price ($)',
                data: prices,
                backgroundColor: 'rgba(168, 85, 247, 0.6)',
                borderColor: '#a855f7',
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: 'inherit' } }
            },
            scales: {
                y: { grid: { color: 'rgba(128, 128, 128, 0.1)' }, ticks: { color: 'inherit' } },
                x: { grid: { display: false }, ticks: { color: 'inherit' } }
            }
        }
    });
}

elements.predictBtn.addEventListener('click', runPrediction);
init();
