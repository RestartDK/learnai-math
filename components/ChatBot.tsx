"use client";

import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Sigma, SearchCheck } from "lucide-react";
import { Bot } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getAIHistory, sendPrompt, sendQuestionAnswers } from "@/utils/sendPrompt";
import { PromptResponse, ResponseBoxProps } from "@/lib/types";

function ResponseBox({ response }: ResponseBoxProps) {
    const sections = response.ai_response.split(/(Question \d+:|question \d+:|Question:|Explanation:|Correction:|Additional Exercise:)/).filter(Boolean);

    return (
        <div className="flex py-4 border-b place-content-start border-gray-500">
            <div className="px-4">
                <Bot size={24} />
            </div>
            <div className="flex-1">
                {sections.map((section, index) => (
					<>
						<p key={index} className="break-words overflow-hidden">
							{section}
						</p>
						<br />
					</>
                ))}
            </div>
        </div>
    );
}

export default function Chatbot() {
	const queryClient = useQueryClient();
	const { data, isLoading, error } = useQuery({ queryKey: ['history'], queryFn: () => getAIHistory() });
	const [input, setInput] = useState<string>("");


	// Can put into custom hooks after
	const mutationKnowledgePrompt = useMutation({
		mutationKey: ["initial"],
		mutationFn: (promptData: string) => sendPrompt(promptData),
		onSuccess: () => {
			queryClient.invalidateQueries({queryKey: ['history']});
		},
		onError: (error) => {
			console.log("Error: ", error);
		},
	});

	const mutationCheckingPrompt = useMutation({
		mutationKey: ["prompt"],
		mutationFn: (promptData: string) => sendQuestionAnswers(promptData),
		onSuccess: () => {
			queryClient.invalidateQueries({queryKey: ['history']});
		},
		onError: (error) => {
			console.log("Error: ", error);
		},
	});

	
	const handleContextSubmit = () => {
		if (input.trim()) {
			mutationKnowledgePrompt.mutate(input);
			setInput("");
		}
	};

	const handleAnswerSubmit = () => {
		if (input.trim()) {
			mutationCheckingPrompt.mutate(input);
			setInput("");
		}
	}

	if (isLoading) {
		return (
			<div>
                Loading...
            </div>
		);
	}

    if (error) {
        return (
            <div>
                Error: {error.message}
            </div>
        );
    }

    if (!data) {
        return (
            <div>
                Error: No data found
            </div>
        );
    }

	return (
		<main className="flex min-h-screen flex-col items-center justify-between py-12">
			<div className="flex flex-col md:w-1/2 w-full">
				{data.map((response, index) => (
					<ResponseBox key={index} response={response} />
				))}
			</div>
			<div className="flex md:w-1/2 w-full gap-2 pt-12">
				<Input 
					className="border-gray-500 bg-transparent flex-1" 
					value={input} 
					onChange={(e) => setInput(e.target.value)}
				/>
				<Button
					className="bg-gray-500 hover:bg-gray-400"
					onClick={handleContextSubmit}
				>
					<Sigma size={24} />
				</Button>
				<Button
					className="bg-gray-500 hover:bg-gray-400"
					onClick={handleAnswerSubmit}
				>
					<SearchCheck size={24} />
				</Button>
			</div>
		</main>
	);
}
