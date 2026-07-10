console.log("MoodLens AI başlatıldı.");

const emotionMap = {
    sadness: {
        name: "😢 Üzüntü",
        color: "#60a5fa"
    },
    anxiety: {
        name: "😰 Kaygı",
        color: "#fb923c"
    },
    loneliness: {
        name: "🥺 Yalnızlık",
        color: "#a78bfa"
    },
    anger: {
        name: "😡 Öfke",
        color: "#ef4444"
    },
    happiness: {
        name: "😊 Mutluluk",
        color: "#facc15"
    },
    stress: {
        name: "🤯 Stres",
        color: "#f97316"
    },
    fear: {
        name: "😨 Korku",
        color: "#f87171"
    },
    disappointment: {
        name: "😞 Hayal Kırıklığı",
        color: "#94a3b8"
    },
    calm: {
        name: "😌 Sakinlik",
        color: "#22c55e"
    },
    confidence: {
        name: "💪 Özgüven",
        color: "#3b82f6"
    }
};


// Greeting Service
async function sayHello() {

    try {

        const name = document.getElementById("name").value;

        const response = await fetch(
            `http://localhost:3000/hello?name=${name}`
        );

        const data = await response.json();

        document.getElementById("helloResult").innerHTML =
            `👋 ${data.message}`;

    }

    catch (error) {

        document.getElementById("helloResult").innerHTML =
            `<span style="color:red;">${error.message}</span>`;

    }

}


// AI Emotion Analysis

const btn = document.getElementById("analyzeBtn");

btn.onclick = async () => {

    const text = document.getElementById("emotionText").value.trim();

    if (text === "") {

        alert("Lütfen analiz edilecek bir metin gir.");

        return;

    }

   btn.disabled = true;

btn.innerHTML = "⏳ Analiz ediliyor...";

document.getElementById("emotionResult").innerHTML = `

<div class="loading">

🤖 AI analiz ediyor...

</div>

`;

try {

    const response = await fetch(
            "http://localhost:8000/predict",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })

            }

        );

        const data = await response.json();
console.log("Backend cevabı:", data);
        const emotion = emotionMap[data.main_emotion];

        document.getElementById("emotionResult").innerHTML = `

<div class="result-card">

    <h2>🧠 Analiz Sonucu</h2>

    <h3 style="color:${emotion.color};">
        ${emotion.name}
    </h3>

    <p>
        <strong>Güven:</strong>
        ${(data.confidence * 100).toFixed(1)}%
    </p>

    <div class="bar">

        <div
            class="fill"
            style="
                width:${data.confidence * 100}%;
                background:${emotion.color};
            "
        ></div>

    </div>

    <h3>📊 En Güçlü 3 Duygu</h3>

    ${data.top_emotions.map(item => {

        const e = emotionMap[item.name];

        return `

        <div class="emotion">

            <span>${e.name}</span>

            <strong>${item.score}%</strong>

        </div>

        `;

    }).join("")}

    <div class="insight">

        💡 ${data.insight}

    </div>
<div class="ai-response">

    🤖 <strong>AI Yorumu</strong>

    <p>
        ${data.ai_response}
    </p>

</div>
</div>

`;

    }

    catch (error) {

        console.error(error);

        document.getElementById("emotionResult").innerHTML = `

<div class="result-card">

<h3 style="color:red;">
❌ AI servisine bağlanılamadı.
</h3>

<p>
Lütfen AI sunucusunun çalıştığını kontrol et.
</p>

</div>

`;

    }

    btn.disabled = false;

    btn.innerHTML = "🔍 Analiz Et";

};const chatBtn = document.getElementById("chatBtn");
const chatBox = document.getElementById("chatBox");

chatBtn.onclick = () => {
    chatBox.classList.toggle("hidden");
};


document.getElementById("sendChatBtn").onclick = async () => {

    const input = document.getElementById("chatInput");
    const message = input.value.trim();

    if(message === "") return;


    const chatMessages = document.getElementById("chatMessages");


    chatMessages.innerHTML += `
        <p>👤 ${message}</p>
    `;


    input.value = "";

chatMessages.innerHTML += `
    <div id="typing" class="ai-message">
        🤖 Yazıyor...
    </div>
`;
    const response = await fetch(
        "http://localhost:8000/chat",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                text:message
            })
        }
    );


    const data = await response.json();
document.getElementById("typing").remove();

    chatMessages.innerHTML += `
        <p>🤖 ${data.response}</p>
    `;

};