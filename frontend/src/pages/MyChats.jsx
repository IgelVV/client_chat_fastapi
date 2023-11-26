import { useState, useEffect } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
// import axios from "../api/axios";
import api from "../api/axios";

import { getLocalAuth} from "../context/AuthProvider";

const ALL_CHATS_URL = '/chat'


const MyChats = () => {
    const [myChats, setMyChats] = useState();
    const axiosPrivate = api;
    const navigate = useNavigate();
    const location = useLocation();
    const auth = getLocalAuth();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const getMyChats = async () => {
            try {
                const response = await axiosPrivate.get(ALL_CHATS_URL, {
                    signal: controller.signal
                });
                isMounted && setMyChats(
                    response.data.filter(function (chat) {
                        return chat.admin === auth.username;
                    })
                );
            } catch (err) {
                console.error(err);
                navigate('/login', { state: { from: location }, replace: true });
            }
        }

        getMyChats();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, [auth.username, location, navigate, axiosPrivate])

    return (
        <article>
            <h2>My Chats</h2>
            {myChats?.length
                ? (
                    <ul>
                        {
                            myChats.map(
                                (chat, i) => <li key={i}>
                                    <Link to={"/chat/" + chat.id}>
                                        {chat.id}. {chat.customer} - {chat.admin}
                                    </Link>
                                </li>
                            )
                        }
                    </ul>
                ) : <p>No chats to display</p>
            }
        </article>
    );
};

export default MyChats;