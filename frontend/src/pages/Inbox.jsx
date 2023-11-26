import { useState, useEffect } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import api from "../api/axios";

const ALL_CHATS_URL = '/chat'


const Inbox = () => {
    const [inbox, setInbox] = useState();
    const axiosPrivate = api;
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const getInbox = async () => {
            try {
                const response = await axiosPrivate.get(ALL_CHATS_URL, {
                    signal: controller.signal
                });
                isMounted && setInbox(
                    response.data.filter(function (chat) {
                        return chat.admin === null;
                    })
                );
            } catch (err) {
                console.error(err);
                navigate('/login', { state: { from: location }, replace: true });
            }
        }

        getInbox();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, [axiosPrivate, location, navigate])

    return (
        <article>
            <h2>Inbox</h2>
            {inbox?.length
                ? (
                    <ul>
                        {
                            inbox.map(
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

export default Inbox;