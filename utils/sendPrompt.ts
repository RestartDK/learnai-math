import { AIResponseHistory, PromptResponse } from "@/lib/types";
import axios from "axios";

export async function sendPrompt(prompt: string): Promise<PromptResponse> {
    try {
        const res = await axios.post(`api/sendPrompt?message=${prompt}`);
        return res.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error("Error in sendPrompt API call:", error.response?.data || error.message);
        } else {
            console.error("Non-Axios error in sendPrompt:", error);
        }
        throw error; 
    }
}

export async function sendQuestionAnswers(prompt: string): Promise<PromptResponse> {
    try {
        const res = await axios.post(`api/checkAnswers?answers=${prompt}`);
        return res.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error("Error in sendPrompt API call:", error.response?.data || error.message);
        } else {
            console.error("Non-Axios error in sendPrompt:", error);
        }
        throw error; 
    }
}

export async function getAIHistory(): Promise<AIResponseHistory> {
    try {
        const res = await axios.get(`api/getAIHistory`);
        return res.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error("Error in getAIHistory API call:", error.response?.data || error.message);
        } else {
            console.error("Non-Axios error in getAIHistory:", error);
        }
        throw error; 
    }
}