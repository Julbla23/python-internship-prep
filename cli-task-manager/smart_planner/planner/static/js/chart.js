const categoryDataElement = document.getElementById("category-data")
const categoryData = JSON.parse(categoryDataElement.textContent)
const labels = categoryData.map(item => item["category__name"]);
const data = categoryData.map(item => item["count"]);
const categoryChart = document.getElementById("categoryChart")

new Chart(categoryChart, {
    type: "bar",
    data: {
        labels: labels,
        datasets: [
            {
                label: "Wykonane taski",
                data: data
            }
        ]
    }
});

const donetaskDataElement = document.getElementById("donetask-data");
const donetaskData = JSON.parse(donetaskDataElement.textContent);
const dayLabels = donetaskData.map(item => item["day"]);
const dayData = donetaskData.map(item => item["count"]);
const donetaskChart = document.getElementById("doneTasksChart");

new Chart(donetaskChart, {
    type: "line",
    data: {
        labels: dayLabels,
        datasets: [
            {
                label: "Zrobione taski",
                data: dayData
            }
        ]
    }
});