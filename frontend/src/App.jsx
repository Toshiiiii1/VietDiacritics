import React, { useState } from "react";
import axios from "axios";
import Spinner from "./components/Spinner.jsx";

const DiacriticsConverter = () => {
	const [inputText, setInputText] = useState("");
	const [outputText, setOutputText] = useState("");
    const [loading, setLoading] = useState(false);

	const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

		try {
			const response = await axios.post(
				"http://127.0.0.1:8000/api/add_diacritics/",
				{
					text: inputText,
				}
			);
			setOutputText(response.data.text_with_diacritics);
		} catch (error) {
			console.error("Error:", error);
		}

        setLoading(false);
	};

	return (
		<div>
			<h1>Chuyển văn bản không dấu sang văn bản có dấu</h1>
			<form onSubmit={handleSubmit}>
				<textarea
                    className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
					value={inputText}
					onChange={(e) => setInputText(e.target.value)}
					placeholder="Nhập văn bản không dấu..."
					rows={4}
					cols={50}
                    required={true}
				/>
				<br />
				<button type="submit">Chuyển đổi</button>
			</form>
			<br />
            {loading ? <Spinner/> : (
				<div>
					<h3>Kết quả:</h3>
					<p>{outputText}</p>
				</div>
			)}
		</div>
	);
};

export default DiacriticsConverter;
