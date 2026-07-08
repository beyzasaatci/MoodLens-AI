async function sayHello() {
    try {
        const name = document.getElementById("name").value;

        const response = await fetch(`http://localhost:3000/hello?name=${name}`);

        const data = await response.json();

        document.getElementById("result").innerText = data.message;
    } catch (error) {
        console.error(error);
        document.getElementById("result").innerText = "Hata: " + error.message;
    }
}