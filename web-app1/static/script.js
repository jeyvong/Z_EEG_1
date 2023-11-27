// script.js

let simulationInterval;
let currentFrameId = 0;

function updateTableWithData(data) {
  // Здесь мы обновим HTML таблицы данными, которые мы получили
  // data - это объект с полями probe, xgboost, ltsm, cnn, содержащий данные из CSV-файлов

  document.getElementById("id_probe_handstart").textContent = data.probe.HandStart;

}

// Функция для выполнения AJAX-запроса на сервер и получения данных для конкретного id_num
function fetchDataForIdNum(id_num) {
  fetch(`/data/${id_num}`)
    .then(response => response.json())
    .then(data => {
      updateTableWithData(data);
      // Здесь мы можем вызвать следующий запрос, если требуется продолжить автоматическую итерацию
      // fetchDataForIdNum(id_num + 1); // Это будет вызывать функцию рекурсивно для следующего id_num
    })
    .catch(error => console.error('Error fetching data:', error));
}


let currentIdNum = 0;


function startSimulation() {
  // Запускаем цикл запросов
  fetchDataForIdNum(currentIdNum);
}

// Функция остановки симуляции, если это необходимо
function stopSimulation() {
// Здесь мы остановим цикл запросов, например, сбросив currentIdNum или используя другой флаг
}


function startSimulation() {
    stopSimulation();
    simulationInterval = setInterval(() => {
        updateTable(currentFrameId);
        currentFrameId++;
    }, 50);  // 0.5 секунды между итерациями
}

function stopSimulation() {
    clearInterval(simulationInterval);
}

function updateTable(frameId) {
    fetch(`/data/${frameId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('timeFrame').value = `id_num: ${data.id_num}`;

            // Обновляем таблицу для каждой модели
            updateEventTable(data.probe, 'Measured Events');
            updateEventTable(data.xgboost, 'Gradient Boosting');
            updateEventTable(data.ltsm, 'LTSM');
            updateEventTable(data.cnn, 'CNN');
        })
        .catch(error => console.error('Ошибка:', error));
}

function updateEventTable(events, modelName) {

    const table = document.getElementById('eventTable');
    const row = table.querySelector(`tr[data-model='${modelName}']`);
    row.cells[1].textContent = events['HandStart'] || 0;
    row.cells[2].textContent = events['FirstDigitTouch'] || 0;
    row.cells[3].textContent = events['BothStartLoadPhase'] || 0;
    row.cells[4].textContent = events['LiftOff'] || 0;
    row.cells[5].textContent = events['Replace'] || 0;
    row.cells[6].textContent = events['BothReleased'] || 0;
}

// Подключаем обработчики к кнопкам
document.getElementById('startButton').addEventListener('click', startSimulation);
document.getElementById('stopButton').addEventListener('click', stopSimulation);
