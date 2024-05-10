// PollPage.js
import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';

import '../styles/styles.css';
const pseuso_json = require("../pseudo-env.json");
const api_host = pseuso_json['api-host']

const PollPage = () => {
	const [pollData, setPollData] = useState({ text: "Идёт отправка запроса..." });
	// const navigate = useNavigate();

	useEffect(() => {
		document.title = "Оценка качества суммаризатора"

		fetch(api_host + 'poll')
			.then(response => response.json())
			.then(data => setPollData(data))
			.catch(error => console.error('Error fetching polls:', error));
	}, []);

	const handleClick = (color) => {
		fetch(api_host + 'poll', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				success: pollData.good_color === color,
				percents: pollData.perc
			})
		}).then(() => {
			alert(`Моя программа оценивает ${pollData.good_color === 'blue' ? 'синее' : 'красное'} ценнее на ${pollData.perc}%`);
			window.location.reload();
			// navigate('./');
		}).catch((error) => {
			alert(`Ошибка: ${error}`);
		})
	};

	return (
		<>
			<h1>Опрос</h1>
			<div className="block-container">
				<p>Выберите фрагмент, наиболее полно передающий смысл текста</p>
				<div className='text-area-like' dangerouslySetInnerHTML={{ __html: pollData.text }}></div>
			</div >
			<div style={{ display: "flex" }}>
				<button className='submit-button button-blue' id='blue' onClick={() => handleClick('blue')}>Синий важнее</button>
				<button className='submit-button button-red' id='red' onClick={() => handleClick('red')}>Красный важнее</button>
			</div>
		</>
	);
};

export default PollPage;
