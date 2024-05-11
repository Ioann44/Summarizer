// SearchPage.js
import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';

import '../styles/styles.css';
import TextWithHighlightedWords from '../components/TextHighlighted';
const pseuso_json = require("../pseudo-env.json");
const api_host = pseuso_json['api-host']

var notificationContainer;
var resultTextArea;
var modalWindow;

const SearchPage = () => {
	const [text, setText] = useState("Котята – это воплощение нежности и игривости. Их пушистая шерсть, маленькие лапки и любопытные глазки сразу растрогают сердце. Когда они родятся, они такие маленькие, что помещаются в ладони, их глазки закрыты, и они полностью зависят от матери. По мере того как котята растут, они начинают исследовать мир вокруг себя. Их игры полные бесконечной энергии и веселья, они ловко ловят игрушки и мячи, учатся охотиться и лазать по деревьям. Когда котята устают от своих приключений, они ищут уютное место для сна – это может быть ваша постель или мягкая корзина. Котята обладают уникальными характерами – некоторые из них могут быть смелыми и дерзкими, другие более робкими и застенчивыми. Однако все они нуждаются в заботе и внимании, чтобы вырасти здоровыми и счастливыми. Наблюдать за игрой котят – это настоящее удовольствие, их беззаветная любовь к вам согреет ваше сердце. Познакомьтесь с этими милыми созданиями, и вы обнаружите, как они способны принести в вашу жизнь много радости и счастья.");
	const [keyWord, setKeyWord] = useState("Кошка");
	const [wordWithGrade, setWordWithGrade] = useState([]);
	const [resText, setResText] = useState("");
	// const navigate = useNavigate();

	useEffect(() => {
		document.title = "Поиск синонимов"

		notificationContainer = document.getElementById("notificationContainer");
		resultTextArea = document.getElementById("compressed-text");
		modalWindow = document.getElementById("modal");
	}, []);

	/**
	 * Fetch cover for suppressing code amount
	 * @param {string} url
	 * @param {boolean} respIsJson
	 * @param {content} init {method: string, headers: {Content-Type: string}, body: string}
	 * @param {function} callback 
	 * @param {string} err_message replaces error message if specified, "don't show" silents any error message
	 * @param {boolean} is_summ_req if true, produces more notifications and blocks/unblocks summarize button 
	*/
	function fetch_template(url, respIsJson, init, callback, err_message = null, is_summ_req = false) {
		if (is_summ_req) {
			document.getElementById("submit-button").disabled = true;
			showTemporaryNotification("Запрос отправлен, обработка может занять несколько минут", 4500);
		}
		fetch(url, init).then(
			response => {
				if (!response.ok) {
					return response.text().then(errorMessage => {
						throw new Error(errorMessage);
					});
				}
				if (is_summ_req) {
					document.getElementById("submit-button").disabled = false;
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
			} else if (err_message !== "don't show") {
				showTemporaryNotification(err_message);
			}
			if (is_summ_req) {
				document.getElementById("submit-button").disabled = false;
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
			setText(event.target.result);
		};
		reader.readAsText(file, 'UTF-8');
	}

	function handleSubmit(event) {
		event.preventDefault();

		const [input_text, preffered_method, compression_mul] = [
			...document.getElementsByClassName("form-input")
		].map(element => element.value)

		if (input_text.length > 1048576) {
			showTemporaryNotification("Текст превышает максимальный размер в 1 миллион символов (2 МБ в кодировке UTF-8)", 6000);
			return;
		}

		fetch_template(api_host + "search", true, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ text: text, word: keyWord })
		}, data => {
			setResText(text);
			setWordWithGrade(data.words);
			if (data.info_msg) {
				showTemporaryNotification(data.info_msg, 6000);
			}
		}, null, true);
	}

	function fileClickAreaHandler() {
		document.getElementById('file-input').click();
	}

	return (
		<>
			<div id="notificationContainer"></div>

			<header>
				<h1>Поиск синонимов</h1>
				<button id="ref-button" onClick={showModal}>?</button>
			</header>

			<div id="modal" style={{ display: 'none' }} onClick={() => (document.getElementById('modal').style.display = 'none')}>
				<div className="modal-content">
					<p>Для поиска схожих по смыслу слов используются обученные векторные представления</p>
					<p>Если вы хотите использовать загрузку файла, убедитесь что его кодировка UTF-8.</p>
					<p>В соответствующем поле нужно написать одно слово, по которому будет производиться поиск</p>
				</div>
			</div>

			<input type="file" id="file-input" style={{ display: 'none' }} accept=".txt" onChange={handleFileInputChange}></input>

			<div className="block-container">
				<form onSubmit={event => handleSubmit(event)}>
					<label className="form-label" htmlFor="source_text" style={{ display: 'inline' }}>Текст для поиска синонимов: </label>
					<p className="file-click-area" style={{ display: 'inline' }} onClick={fileClickAreaHandler}>(вы можете перетащить файл в область ниже или нажать
						сюда для выбора файла)</p>
					<textarea
						className="form-input file-drop-area" style={{ width: '100%' }} id="source_text" rows="10"
						maxLength="1048576" onDrop={handleFileDrop} onDragOver={(event) => event.preventDefault()}
						value={text} onChange={e => { setText(e.target.value) }}>
					</textarea>
					<label className="form-label" htmlFor="source_text" style={{ marginBottom: "0px" }}>Искомое слово:</label>
					<input type='text' className='text-area-like-input' value={keyWord} onChange={e => setKeyWord(e.target.value)}></input>
					<button id="submit-button" type="submit">Отправить</button>
				</form>
			</div>

			<div className="block-container">
				<p>Обработанный текст:</p>
				<TextWithHighlightedWords text={resText} wordsToHighlight={wordWithGrade} />
			</div>
		</>
	);
};

export default SearchPage;
