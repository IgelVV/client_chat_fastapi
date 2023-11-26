import { useState, useEffect, useRef } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import api from "../api/axios";

import { useParams } from 'react-router';
import { getLocalAuth } from "../context/AuthProvider"



const Chat = () => {
    const [chat, setChat] = useState();
    const [ws, setWs] = useState([]);
    const [messages, setMessages] = useState([]);
    const axiosPrivate = api;
    const params = useParams();
    const auth = getLocalAuth();
    const inputRef = useRef(null);

    const sendMessage = (event) => {
        console.log(`send ${inputRef.current.value}`);
        console.log(chat);
        ws.send(inputRef.current.value);
        inputRef.current.value = "";
    };



    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const acceptChat = async () => {
            try {
                setChat(params.id)
                const response = await axiosPrivate.get('/chat/' + params.id + '/accept', {
                    signal: controller.signal
                });
                console.log(response)
            } catch (err) {
                console.error(err);
            }
        }

        const createChat = async () => {
            try {
                const response = await axiosPrivate.post('/chat/', {}, {
                    signal: controller.signal
                });
                // console.log(getLocalAuth())
                // console.log(response)
                console.log("createChat", response.data.id)
                isMounted && setChat(response.data.id);
            } catch (err) {
                console.error(err);
            }
        }

        const getChatHistori = async () => {
            try {
                const response = await axiosPrivate.get('/chat/' + params.id + '/history', {
                    signal: controller.signal
                });
                setMessages((prevMessages) => [...prevMessages, ...response.data]);
                console.log(response);
            } catch (err) {
                console.error(err);
            }
        }


        if (auth.isAdmin) {
            acceptChat();
        } else {
            createChat();
        }

        getChatHistori();

        const socket = new WebSocket(`ws://${window.location.hostname}:8000/chat/ws/${params.id}/${auth.accessToken}`);
        console.log(socket)
        socket.onmessage = function (event) {
            console.log(event.data);
            let userdata = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, userdata]);
            // let client_usernames = [...userdata.usernames];
            // setUsernames(client_usernames)
        };
        setWs(socket);

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, []);


    return (
        <div className="">
            <h2>Chat {chat}</h2>
            <div className="mb-3">
                <h2>Hallo {auth.username}</h2>
                <input ref={inputRef} type="text" className="form-control" />
                <button onClick={sendMessage} className="btn btn-primary">Send</button>
            </div>
            <ul>
                    {messages.map(
                        (message, index) => {
                            return(<li key={index}>{`${message.from_user}: ${message.text}`}</li>)
                        }
                    )}
            </ul>
        </div>
    );
};

export default Chat;