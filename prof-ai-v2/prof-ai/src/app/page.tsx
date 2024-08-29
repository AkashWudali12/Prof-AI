import { ChatBox } from "@/components/chat-box";
import { Analytics } from '@vercel/analytics/react';

export default function Chat() {
    return (
        <>
            <ChatBox />
            <Analytics />
        </>
    )
}