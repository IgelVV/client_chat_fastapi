import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/axios";

import { getLocalAuth } from "../context/AuthProvider"



const User = () => {
    const [chat, setChat] = useState();

    const axiosPrivate = api;
    const auth = getLocalAuth();

    const navigate = useNavigate();


    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const createChat = async () => {
            try {
                const response = await axiosPrivate.post('/chat/', {}, {
                    signal: controller.signal
                });
                console.log("createChat", response.data.id)
                isMounted && setChat(response.data.id);
                return response.data.id;
            } catch (err) {
                console.error(err);
            }
        }

        if (auth.isAdmin) {
            navigate("/admin")
        } else {
            createChat();
        }

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, []);


    return (
        <div className="">
            <h2>User menu</h2>
            <span className="line">
                <Link to={"/chat/"+chat}>Service Chat</Link>
            </span>
        </div>
    );
};

export default User;