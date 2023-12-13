"use client";

import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Sigma } from "lucide-react";
import { User } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { sendPrompt } from "@/utils/sendPrompt";
import { PromptResponse, ResponseBoxProps } from "@/lib/types";

function ResponseBox({ response }: ResponseBoxProps) {
	return (
		<div className="flex py-4 border-b place-content-start border-gray-500">
			<div className="py-2 px-4">
				<User size={24} />
			</div>
			<p className="flex-1 break-words overflow-hidden">{response}</p>
		</div>
	);
}

export default function Chatbot() {
	const [input, setInput] = useState<string>("");
	const [responses, setResponses] = useState<PromptResponse[]>([]);	// Because I got no db rn bruh

	const mutationPrompt = useMutation({
		mutationKey: ["prompt"],
		mutationFn: (promptData: string) => sendPrompt(promptData),
		onSuccess: (data) => {
			setResponses(currentResponses => [...currentResponses, data]);
		},
		onError: (error) => {
			console.log("Error: ", error);
		},
	});
	
	const handleSubmit = () => {
		if (input.trim()) {
			mutationPrompt.mutate(input);
			setInput("");
		}
	};

	return (
		<main className="flex min-h-screen flex-col items-center justify-between py-12">
			<div className="flex flex-col md:w-1/2 w-full">
				{responses.map((response, index) => (
					<ResponseBox key={index} response={response.response} />
				))}
			</div>
			<div className="flex md:w-1/2 w-full gap-2">
				<Input 
					className="border-gray-500 bg-transparent flex-1" 
					value={input} 
					onChange={(e) => setInput(e.target.value)}
				/>
				<Button
					className="bg-gray-500 hover:bg-gray-400"
					onClick={handleSubmit}
				>
					<Sigma size={24} />
				</Button>
			</div>
		</main>
	);
}
