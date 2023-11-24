import { useRef, useState, useEffect } from "react";
import useAuth from "../hooks/useAuth";
import localAuthName from "../hooks/useAuth";
import {setObjectInLocalStorage} from "../utils/localStorageManager"
import { Link, useNavigate, useLocation } from 'react-router-dom';
import axios from "../api/axios";

const LOGIN_URL = '/auth/login/'


const Login = () => {
    const {setAuth} = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";

    const userRef = useRef(); 
    const errRef = useRef();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        setErrMsg('');
    }, [username, password]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log(username, password);
        try {
            const response = await axios.post(
                LOGIN_URL,
                {username, password},
                {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
                    withCredentials: true
                }
            )
            console.log(response);
            console.log(JSON.stringify(response));
            const accessToken = response?.data?.access_token;
            const isAdmin = response?.data?.is_admin;
            setAuth({username, password, isAdmin, accessToken});
            setObjectInLocalStorage(localAuthName, {username, password, isAdmin, accessToken});
            // navigate(from, { replace: true });
            navigate("/")
        } catch (err) {
            console.log(err);
            if (!err?.response) {
                setErrMsg('No Server Response');
            } else if (err.response?.status === 401) {
                setErrMsg('Wrong Username or password');
            } else {
                setErrMsg("Login faild");
            }
            errRef.current.focus();
        };
    };

    return (
        <section>
            <p ref={errRef} className={errMsg ? "text-danger" : 
            "text-primary"} aria-live="assertive">{errMsg}</p>
            <h1>Login</h1>
            <div>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="username">Username:</label>
                        <input
                            className="form-control"
                            type="text" 
                            id="username"
                            ref={userRef}
                            autoComplete="off"
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="password">Password:</label>
                        <input 
                            className="form-control"
                            type="password" 
                            id="password"
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <button className="btn btn-primary">Sign In</button>
                    </div>
                </form>
                <p>
                <span className="line">
                    <Link to="/register">Register</Link>
                </span>
                </p>
            </div>
            
        </section>
    )
}
export default Login