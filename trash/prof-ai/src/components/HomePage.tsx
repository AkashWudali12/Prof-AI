import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/ChatBox.css';
import { Professor } from './types/Professor';

const ChatBox: React.FC = () => {
    const [message, setMessage] = useState<string>('');
    const [file, setFile] = useState<File | null>(null);

    const navigate = useNavigate();

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(event.target.value);
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFile(event.target.files ? event.target.files[0] : null);
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        var formData = new FormData();
        formData.append('message', message);
        formData.append('test', "jfojrwfojeojojeo")
        if (file) formData.append('file', file);

        const my_message = formData.get('message');
        console.log('Message in FormData:', my_message);

        try {
            const response = await fetch('http://127.0.0.1:5000/get_professor_description', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            console.log('Server response:', data.response);

            const profs: Professor[] = data.response.map((prof: any) => ({
                name: prof.name,
                description: prof.description,
                image_file_path: prof.picture
            }));

            navigate('browse_profs', { state: { prof_list: profs } });
            setMessage(''); // Reset message input after submission
            setFile(null); // Reset file input after submission
        } catch (error) {
            console.error('Error sending message:', error);
            navigate('browse_profs', {});
            setMessage(''); // Reset message input after submission
            setFile(null); // Reset file input after submission
        }
    };

    return (
        <div className="chatbox-container">
            <form onSubmit={handleSubmit}>
                <label htmlFor="chatbox">
                    Describe your research interests, skills, and work experience or attach your resume:
                </label>
                <textarea
                    id="chatbox"
                    value={message}
                    onChange={handleChange}
                    placeholder="Type your message here..."
                />
                <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                />
                <button type="submit">Get Relevant Professors</button>
            </form>
        </div>
    );
};

export default ChatBox;
