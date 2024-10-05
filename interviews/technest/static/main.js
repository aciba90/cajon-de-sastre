/** Main JavaScript - It fetches and renders graphs. */

/**
 * Creates a new Bar Chart.
 * @param {string} elementId - Element Id of the html canvas to inject the graph in.
 * @param {Array<string>} labels - Labels of the X dimension.
 * @param {Array<number>} data - Data of the Y dimension.
 * @param {string} label - Label of the chart.
 * @returns reference to the chart.
 */
function createChart(elementId, labels, data, label) {
    const context = document.getElementById(elementId);
    graphConfig = {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: label,
                data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    stacked: false,
                    beginAtZero: true,
                    ticks: {
                        autoSkip: false,
                        maxRotation: 70,
                        minRotation: 70
                    }
                },
            },
            responsive: true,
            maintainAspectRatio: false,
        },
    };
    const graphChart = new Chart(context, graphConfig);
    return graphChart;
}

/**
 * Fetches an url.
 * @param {string} url - Url to fetch.
 * @returns response
 */
async function fetchUrl(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

/**
 * Injects a Graph taken from `url` in the html element associated with `elementId`.
 * @param {string} url - Url to fetch the graph data from.
 * @param {string} elementId - ElementId to inject the graph in.
 */
function injectGraph(url, elementId) {
    fetchUrl(url)
        .then(data => createChart(elementId, data.data_x, data.data_y, data.name))
        .catch(err => {
            console.warn(err);
            return;
        });
}

/**
 * Fetches the graph data and injects a graph chart into each canvas element.
 */
function main() {
    document.querySelectorAll(".container-graph canvas").forEach(
        canvas => injectGraph(canvas.dataset.graphUrl, canvas.id)
    );
}

window.onload = main;
