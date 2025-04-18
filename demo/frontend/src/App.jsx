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
		<>
			<div className="container mx-auto mt-8">
				<h1 className="text-center text-3xl font-bold">
					Chuyển văn bản tiếng Việt không dấu sang văn bản có dấu
				</h1>
				<form
					onSubmit={handleSubmit}
					className="flex flex-col items-center mt-4"
				>
					<textarea
						className="border border-gray-300 rounded-md p-2 w-1/2"
						value={inputText}
						onChange={(e) => setInputText(e.target.value)}
						placeholder="Nhập văn bản không dấu..."
						rows={4}
						cols={50}
						required={true}
					/>
					<br />
					<button
						type="submit"
						className="mt-4 bg-blue-500 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-600"
						disabled={loading}
					>
						{loading ? "Đang xử lý..." : "Thêm dấu"}
					</button>
				</form>
				<br />
				{loading && <Spinner />}
				{outputText && (
					<div className="mt-4 text-center">
						<p className="font-bold">Kết quả:</p>
						<p>{outputText}</p>
					</div>
				)}
			</div>
		</>
	);
};

export default DiacriticsConverter;
