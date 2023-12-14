export interface PromptResponse {
    _id: string;
    response: string;
}

export interface AIResponse {
    ai_response: string;
}

export type AIResponseHistory = AIResponse[];

export interface InputPromptsProps {
	message: string;
}

export interface ResponseBoxProps {
	response: AIResponse;
}