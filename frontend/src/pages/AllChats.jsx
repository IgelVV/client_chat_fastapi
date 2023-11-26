import { useState, useEffect } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
// import axios from "../api/axios";
import api from "../api/axios";


const ALL_CHATS_URL = '/chat'


const AllChats = () => {
    const [chats, setChats] = useState();
    const axiosPrivate = api;
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const getAllChats = async () => {
            try {
                const response = await axiosPrivate.get(ALL_CHATS_URL, {
                    signal: controller.signal
                });
                console.log(response.data);
                isMounted && setChats(response.data);
            } catch (err) {
                console.error(err);
                navigate('/login', { state: { from: location }, replace: true });
            }
        }

        getAllChats();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, [])

    return (
        <article>
            <h2>All Chats</h2>
            {chats?.length
                ? (
                    <ul>
                        {
                            chats.map(
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

export default AllChats;