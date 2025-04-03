let player = document.getElementById("player");
let log = document.getElementById("log");
let currentStationIndex = 0;
let stationsList = [];

// Загружаем список станций из JSON-файла
fetch("stations.json")
.then(response => response.json())
.then(data => {
    stationsList = data;
    updateStationsList();
    setInitialStation();
})
.catch(error => {
    console.error("Ошибка при загрузке списка станций:", error);
    logMessage("Ошибка загрузки станций.");
});

// Функция для обновления списка станций в интерфейсе
function updateStationsList() {
    const select = document.getElementById("stations");
    stationsList.forEach((station, index) => {
        let option = document.createElement("option");
        option.value = station.url;
        option.textContent = station.name;
        select.appendChild(option);
    });

    // Добавляем обработчик события для изменения выбора станции
    select.addEventListener("change", (event) => {
        const selectedUrl = event.target.value;
        currentStationIndex = stationsList.findIndex(station => station.url === selectedUrl);
        player.src = selectedUrl;
        player.play();
        logMessage("Смена станции: " + event.target.options[event.target.selectedIndex].text);
    });
}

// Устанавливаем начальную станцию в плеер и отображаем её в списке
function setInitialStation() {
    player.src = stationsList[currentStationIndex].url;
    logMessage("Играет: " + stationsList[currentStationIndex].name);
    // Устанавливаем текущую станцию в выпадающем списке
    const select = document.getElementById("stations");
    select.selectedIndex = currentStationIndex;
}

// Функции для управления плеером
function logMessage(msg) {
    console.log(msg);
    log.textContent += msg + "\n";
}

// Воспроизведение/Пауза
function togglePlay() {
    if (player.paused) {
        player.play();
        logMessage("Играет: " + player.src);
    } else {
        player.pause();
        logMessage("Остановлено");
    }
}

// Следующая станция
function nextStation() {
    currentStationIndex = (currentStationIndex + 1) % stationsList.length;
    player.src = stationsList[currentStationIndex].url;
    player.play();
    logMessage("Смена станции: " + stationsList[currentStationIndex].name);
    // Обновляем выпадающий список
    const select = document.getElementById("stations");
    select.selectedIndex = currentStationIndex;
}

// Предыдущая станция
function prevStation() {
    currentStationIndex = (currentStationIndex - 1 + stationsList.length) % stationsList.length;
    player.src = stationsList[currentStationIndex].url;
    player.play();
    logMessage("Смена станции: " + stationsList[currentStationIndex].name);
    // Обновляем выпадающий список
    const select = document.getElementById("stations");
    select.selectedIndex = currentStationIndex;
}



// Service worker ini
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js')
    .then((registration) => {
        console.log('Service Worker зарегистрирован', registration);
    })
    .catch((error) => {
        console.error('Ошибка регистрации Service Worker:', error);
    });
}
