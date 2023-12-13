"use client";

import Image from "next/image";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Sigma } from "lucide-react";
import { User } from "lucide-react";
import { useState } from "react";
import { sendPrompt } from "@/utils/sendPrompt";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Prompt, PromptResponse, ResponseBoxProps } from "@/lib/types";

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
	const queryClient = useQueryClient();
	const [input, setInput] = useState<string>("");
	const [responses, setResponses] = useState<PromptResponse[]>([]);

	const mutationPrompt = useMutation({
		mutationFn: ({ prompt }: Prompt) => {
			return sendPrompt();
		},
		onSuccess: (data) => {
			setResponses([...responses, data]);
			console.log(responses);
		},
		onError: (error) => {
			// Handle error
			console.log("Error: ", error);
		},
	});

	const handleSubmit = () => {
		mutationPrompt.mutate({ prompt: input });
		setInput("");
	};

	return (
		<main className="flex min-h-screen flex-col items-center justify-between py-12">
			<div className="flex flex-col md:w-1/2 w-full">
				{responses.map((response) => (
					<ResponseBox response={response.message} />
				))}
			</div>
			<div className="flex md:w-1/2 w-full gap-2">
				<Input className="border-gray-500 bg-transparent" />
				<Button
					className="bg-gray-500 hover:bg-gray-400"
					onSubmit={() => handleSubmit}
				>
					<Sigma size={24} />
				</Button>
			</div>
		</main>
	);
}
