import React from 'react';
import TextImageLayout from './TextImageLayout';
import { useLocation } from 'react-router-dom';
import { Professor } from './types/Professor';

const TextImageList: React.FC = () => {
    const location = useLocation();
    const prof_list = location.state?.prof_list as Professor[] | undefined;

    console.log("Got Profs", prof_list)

    return (
        <ul style={{ listStyle: 'none', padding: 0 }}>
            {prof_list ? prof_list.map((item) => (
                <li key={item.name}>
                    <TextImageLayout 
                        mainText={item.name} 
                        // item.image_file_path || 
                        imagePath={"http://127.0.0.1:5000/images/" + item.image_file_path}
                        rightText={item.description}
                    />
                </li>
            )) : <li>No professors found.</li>}
        </ul>
    );
};

export default TextImageList;
