// GenEmailPage.tsx
import React from 'react';
import { useLocation } from 'react-router-dom';

const EmailDisplay: React.FC = () => {
    // Sample email data for demonstration
    const email = {
        sender: "john.doe@example.com",
        recipient: "jane.smith@example.com",
        subject: "Meeting Reminder",
        body: "Hi Jane,\n\nThis is a reminder for our meeting scheduled for tomorrow at 10 AM.\n\nBest,\nJohn",
        timestamp: "2023-07-01 09:00 AM"
    };

    const location = useLocation();
    const email_info = location.state?.email

    return (
        <div className="email-container">
            <div className="email-header">
                <p><strong>From:</strong> {email_info.from}</p>
                <p><strong>To:</strong> {email_info.to}</p>
                <p><strong>Subject:</strong> {email_info.subject}</p>
                <p><strong>Date:</strong> {email.timestamp}</p>
            </div>
            <div className="email-body">
                <p>{email_info.email}</p>
            </div>
        </div>
    );
};

export default EmailDisplay;
