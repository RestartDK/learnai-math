"use client";

import { ReactNode } from "react";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { useState } from "react";

export default function Providers({
	children,
}: {
	children: ReactNode;
}): JSX.Element {
	const [queryClient] = useState(() => new QueryClient());
	return (
		<QueryClientProvider client={queryClient}>
            {children}
        </QueryClientProvider>
	);
}