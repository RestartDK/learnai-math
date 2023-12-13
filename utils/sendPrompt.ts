import { PromptResponse } from "@/lib/types";
import axios from "axios";

export async function sendPrompt(prompt: string):Promise<PromptResponse> {
    const res = await axios.post(`api/test?message=${prompt}`);
    return res.data;
}