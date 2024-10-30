var ctx1 = document.getElementById("lineChart").getContext("2d");
var myChart = new Chart(ctx1, {
    type: "line",
    data: {
        labels: chartLabels,
        datasets: [
            {
                label: "Rapport des projets",
                data: chartProjectData,
                backgroundColor: "#24695c",
                borderColor: "#24695c",
                borderWidth: 2,
                borderDash: [3],
                pointBorderColor: "#24695c",
                pointRadius: 3,
                pointBorderWidth: 1,
                tension: 0.3,
            },
            {
                label: "Rapport des éléments",
                data: chartItemData,
                backgroundColor: "#6f8a85",
                borderColor: "#6f8a85",
                borderWidth: 2,
                borderDash: [0],
                pointBorderColor: "#6f8a85",
                pointRadius: 3,
                pointBorderWidth: 1,
                tension: 0.3,
            }
        ]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: "#7c8ea7",
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return value;
                    },
                    color: "#7c8ea7"
                },
                grid: {
                    drawBorder: true,
                    color: "rgba(132, 145, 183, 0.15)",
                    borderDash: [3],
                    borderColor: "rgba(132, 145, 183, 0.15)"
                }
            },
            x: {
                ticks: {
                    color: "#7c8ea7"
                },
                grid: {
                    display: false,
                    color: "rgba(132, 145, 183, 0.09)",
                    borderDash: [3],
                    borderColor: "rgba(132, 145, 183, 0.09)"
                }
            }
        }
    }
});
