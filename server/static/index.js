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
}