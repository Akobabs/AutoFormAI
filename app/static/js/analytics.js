function initializeAnalytics(data) {
    // Usage Trends Chart (Line Chart)
    const usageChartCtx = document.getElementById('usage-chart').getContext('2d');
    new Chart(usageChartCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Searches Over Time',
                data: [data.database.total_searches, data.database.total_searches + 10, data.database.total_searches + 20, data.database.total_searches + 15, data.database.total_searches + 30, data.database.total_searches + 25],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Category Distribution Chart (Pie Chart)
    const categoryChartCtx = document.getElementById('category-chart').getContext('2d');
    new Chart(categoryChartCtx, {
        type: 'pie',
        data: {
            labels: ['Names', 'Emails', 'General'],
            datasets: [{
                data: [
                    data.database.popular_suggestions.filter(s => s.text.includes('@')).length,
                    data.database.popular_suggestions.filter(s => !s.text.includes('@')).length,
                    data.database.popular_suggestions.length / 3
                ],
                backgroundColor: ['#2563eb', '#10b981', '#f59e0b']
            }]
        },
        options: {
            responsive: true
        }
    });

    // Refresh Button
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/analytics');
                const newData = await response.json();
                initializeAnalytics(newData);
                alert('Analytics refreshed!');
            } catch (error) {
                console.error('Error refreshing analytics:', error);
                alert('Failed to refresh analytics.');
            }
        });
    }

    // Export Button
    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `analytics_${new Date().toISOString()}.json`;
                a.click();
                URL.revokeObjectURL(url);
            } catch (error) {
                console.error('Error exporting analytics:', error);
                alert('Failed to export analytics.');
            }
        });
    }
}