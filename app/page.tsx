import MaxWidthWrapper from "./MaxWidthWrapper";
import Chatbot from "@/components/ChatBot";
import Image from "next/image";
import Link from "next/link";

export default function Home() {
	return (
		<MaxWidthWrapper>
			<Chatbot />
		</MaxWidthWrapper>
	);
}
