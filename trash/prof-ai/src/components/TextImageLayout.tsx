// TextImageLayout.tsx
import React from 'react';
import './styles/TextImageLayout.css';
import { useNavigate } from 'react-router-dom';


interface TextImageLayoutProps {
    mainText: string;
    imagePath: string;
    rightText: string;
}

const TextImageLayout: React.FC<TextImageLayoutProps> = ({ mainText, imagePath, rightText }) => {
    const navigate = useNavigate();

    const handleClick = async () => {
        const data = {
            mainText,
            imagePath,
            rightText
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/generate_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            navigate("/get_email", { state: { email: result } })
            console.log("Response from backend:", result);
        } catch (error) {
            console.error("Error sending data to backend:", error);
            navigate("/get_email", { state: {} })
        }

    };

    return (
        <div className="container" onClick={handleClick}>
            <p className="top-text">{mainText}</p>
            <div className="content">
                <img src={imagePath} alt="Descriptive Alt Text" className="image"/>
                <p className="right-text">{rightText}</p>
            </div>
        </div>
    );
};

export default TextImageLayout;
