import { PromptResponse } from "@/lib/types";
import axios from "axios";

export async function sendPrompt():Promise<PromptResponse> {
    const res = await axios.post('api/prompt');
    return res.data;
}