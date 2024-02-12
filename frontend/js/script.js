// Import the required date adapter from Chart.js
import { Chart, registerables } from 'https://cdn.jsdelivr.net/npm/chart.js';
/* import 'https://cdnjs.cloudflare.com/ajax/libs/chartjs-adapter-date-fns/3.0.0/chartjs-adapter-date-fns.min.js';

// Register the date-fns adapter with Chart.js
Chart.register(...registerables);

// Now you can use Chart.js as usual
fetch('/api/cpi')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('cpiChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => item.date),
                datasets: [{
                    label: 'CPI',
                    data: data.map(item => item.value),
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'month'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'CPI Value'
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching CPI data:', error));
 */