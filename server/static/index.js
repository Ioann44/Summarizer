/**
 * Fetch cover for suppressing code amount
 * @param {string} url
 * @param {boolean} respIsJson
 * @param {content} init {method: string, headers: {Content-Type: string}, body: string}
 * @param {function} callback 
 * @param {string} err_message replaces error message if specified
*/
function fetch_template(url, respIsJson, init, callback, err_message = null) {
	fetch(url, init).then(
		response => {
			if (!response.ok) {
				return response.text().then(errorMessage => {
					throw new Error(errorMessage);
				});
			}
			if (respIsJson) {
				return response.json();
			} else {
				return response.text();
			}
		}
	).then(callback).catch(errorMessage => {
		if (err_message === null) {
			showTemporaryNotification(errorMessage);
		} else {
			showTemporaryNotification(err_message);
		}
	})
}

function showTemporaryNotification(message, duration = 3000) {
	const notification = document.createElement("div");
	notification.textContent = message;
	notification.classList.add("notification");

	notificationContainer.appendChild(notification);
	notification.style.animation = `slide-down 0.5s ease-in-out forwards, fade-out 0.5s ease-in-out ${duration}ms forwards`;

	setTimeout(() => {
		notification.remove()
	}, duration + 1000);
}

function showModal() {
	modalWindow.style.display = "block";
}

function handleFileDrop(event) {
	event.preventDefault();
	const file = event.dataTransfer.files[0];
	readFileContents(file);
}

function handleFileInputChange(event) {
	const file = event.target.files[0];
	readFileContents(file);
}

function readFileContents(file) {
	const reader = new FileReader();
	reader.onload = function (event) {
		const text = event.target.result;
		document.getElementById('source_text').value = text;
	};
	reader.readAsText(file, 'UTF-8');
}

// MARK: History

function toggleHistory() {
    var historyList = document.getElementById("history-list");
    var button = document.querySelector('.toggle-history');

    if (historyList.style.display === 'none' || historyList.style.maxHeight === '0px') {
        historyList.style.display = 'block';
        var maxHeight = historyList.scrollHeight + "px";
        historyList.style.maxHeight = maxHeight;
        button.style.backgroundColor = '#e0e0e0';
    } else {
        historyList.style.maxHeight = '0';
        button.style.backgroundColor = '#f0f0f0';
        setTimeout(function() {
            historyList.style.display = 'none';
        }, 300);
    }
}

function addToHistory(dateTime, text, link) {
    var historyList = document.getElementById("history-list");

    var historyItem = document.createElement("div");
    historyItem.classList.add("history-item");

    var info = document.createElement("div");
    info.classList.add("history-item-info");
    
    var dateElement = document.createElement("div");
    dateElement.classList.add("history-item-date");
    dateElement.textContent = dateTime.toLocaleString();
    
    var textElement = document.createElement("div");
    textElement.classList.add("history-item-text");
	textElement.textContent = text;

    info.appendChild(dateElement);
    info.appendChild(textElement);

    var download = document.createElement("div");
    download.classList.add("history-item-download");
    var downloadLink = document.createElement("a");
    downloadLink.href = link;
    downloadLink.textContent = "Скачать";
    download.appendChild(downloadLink);

    historyItem.appendChild(info);
    historyItem.appendChild(download);

    historyList.appendChild(historyItem);
}

// MARK: Onload

window.onload = () => {
	const notificationContainer = document.getElementById("notificationContainer");
	const resultTextArea = document.getElementById("compressed-text");
	modalWindow = document.getElementById("modal");

	// Update compression multipltiplier listener
	const rangeSliderValueField = document.getElementById("range-value");
	const rangeSlider = document.getElementById("range");
	rangeSlider.addEventListener("input", function () {
		rangeSliderValueField.textContent = rangeSlider.value;
	});

	// Summarize request listener
	document.getElementsByTagName("form")[0].addEventListener("submit", event => {
		event.preventDefault();

		const [input_text, preffered_method, compression_mul] = [
			...document.getElementsByClassName("form-input")
		].map(element => element.value)

		if (input_text.length > 5242880) {
			showTemporaryNotification("Текст превышает максимальный размер в 5 миллионов символов (10 МБ в кодировке UTF-8)", 6000);
			return;
		}

		fetch_template("/api/summarize", true, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ text: input_text, method: preffered_method, compression_mul: compression_mul })
		}, data => {
			resultTextArea.value = data.text;
			resultTextArea.style.height = "0";
			resultTextArea.style.height = resultTextArea.scrollHeight + 3 + "px";
			if (data.info_msg) {
				showTemporaryNotification(data.info_msg, 6000);
			}
		})
	});

	// File loader listener
	document.getElementsByClassName('file-click-area')[0].addEventListener('click', function () {
		document.getElementById('file-input').click();
	});

	// History adding example
	var currentDate = new Date();
	var sampleText = "Некоторый текст для истории.";
	addToHistory(currentDate, sampleText, "123");
}