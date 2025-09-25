const form = document.getElementById("analyze-form");
const resultsDiv = document.getElementById("results");
const loadingDiv = document.getElementById("loading");

let sentimentChart; // store Chart.js instance

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    resultsDiv.style.display = "none";
    loadingDiv.style.display = "block";

    const formData = new FormData(form);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        loadingDiv.style.display = "none";

        if (data.error) {
            alert(data.error);
            return;
        }

        resultsDiv.style.display = "block";

        // ---------------- Sentiment Chart ----------------
        const ctx = document.getElementById("sentimentChart").getContext("2d");
        if (sentimentChart) sentimentChart.destroy();

        const total = data.positive + data.neutral + data.negative;

        sentimentChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Positive", "Neutral", "Negative"],
                datasets: [{
                    label: "Number of Posts",
                    data: [data.positive, data.neutral, data.negative],
                    backgroundColor: ["#4caf50", "#ffeb3b", "#f44336"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    datalabels: {
                        anchor: 'end',
                        align: 'end',
                        color: '#000',
                        font: { weight: 'bold' },
                        formatter: (value) => `${value} (${((value/total)*100).toFixed(1)}%)`
                    }
                }
            },
            plugins: [ChartDataLabels]
        });

        // ---------------- Word Cloud ----------------
        const wordCloudCanvas = document.getElementById("wordCloudCanvas");
        wordCloudCanvas.getContext('2d').clearRect(0, 0, wordCloudCanvas.width, wordCloudCanvas.height);
        WordCloud(wordCloudCanvas, {
            list: data.words.map(([word, count]) => [word, count]),
            gridSize: Math.round(16 * wordCloudCanvas.width / 1024),
            weightFactor: 5,
            fontFamily: 'Segoe UI',
            color: 'random-dark',
            rotateRatio: 0.5,
            backgroundColor: document.body.classList.contains("dark-mode") ? "#2c2c2c" : "#fff"
        });

        // ---------------- Keyword Highlight ----------------
        const highlightKeyword = (text, keyword) => {
            if (!keyword) return text;
            const re = new RegExp(`(${keyword})`, "gi");
            return text.replace(re, '<mark>$1</mark>');
        };

        const positiveList = document.getElementById("positivePosts");
        positiveList.innerHTML = "";
        data.top_positive.forEach(([post, score]) => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.innerHTML = `<details>
                                <summary>[${score}] ${highlightKeyword(post.substring(0, 100), form.keyword.value)}...</summary>
                                ${highlightKeyword(post, form.keyword.value)}
                            </details>`;
            positiveList.appendChild(li);
        });

        const negativeList = document.getElementById("negativePosts");
        negativeList.innerHTML = "";
        data.top_negative.forEach(([post, score]) => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.innerHTML = `<details>
                                <summary>[${score}] ${highlightKeyword(post.substring(0, 100), form.keyword.value)}...</summary>
                                ${highlightKeyword(post, form.keyword.value)}
                            </details>`;
            negativeList.appendChild(li);
        });

    } catch (err) {
        loadingDiv.style.display = "none";
        alert("An error occurred: " + err.message);
    }
});

// ---------------- Dark Mode Toggle ----------------
const darkModeToggle = document.getElementById("darkModeToggle");
darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});

// ---------------- Download Buttons ----------------
document.getElementById("downloadChart").addEventListener("click", () => {
    const a = document.createElement("a");
    a.href = document.getElementById("sentimentChart").toDataURL("image/png");
    a.download = "sentiment_chart.png";
    a.click();
});

document.getElementById("downloadWordCloud").addEventListener("click", () => {
    const a = document.createElement("a");
    a.href = document.getElementById("wordCloudCanvas").toDataURL("image/png");
    a.download = "word_cloud.png";
    a.click();
});
