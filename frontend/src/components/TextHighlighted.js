import React from 'react';
import ReactDomServer from 'react-dom/server';
import "../styles/styles.css"

const TextWithHighlightedWords = ({ text, wordsToHighlight }) => {
	let gradeByWord = new Map(wordsToHighlight);

	function doSpan(word) {
		const brightness = gradeByWord.get(word);
		if (brightness) {
			return ReactDomServer.renderToString(
				<span key={word} className="highlighted-word" title={`${brightness}%`} style={{ backgroundColor: `rgba(0, 255, 0, ${brightness / 50 - 1})` }}>
					{word}
				</span>
			);
		} else {
			return word;
		}
	}

	let res = text.replace(/([а-яёА-ЯЁ]+)/, doSpan);
	return (
		<div className='text-area-like' id="compressed-text" readOnly
			dangerouslySetInnerHTML={{ __html: text.replace(/([а-яёА-ЯЁ]+)/g, doSpan) }}
		></div>
	)
};

export default TextWithHighlightedWords;