import { useRef, useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "../api/axios";

const REGISTER_URL = '/auth/register/'


const Register = () => {
    const navigate = useNavigate();
    const userRef = useRef(); 
    const errRef = useRef();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isAdmin, setIsAdmin] = useState(false);
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        setErrMsg('');
    }, [username, password, isAdmin]);



    const handleCheckboxChange = event => {

        if (event.target.checked) {
            setIsAdmin(true)
          } else {
            setIsAdmin(false)
          }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log(username, password, isAdmin);
        try {
            const response = await axios.post(
                REGISTER_URL,
                JSON.stringify({username, password, is_admin: isAdmin,}),
                {
                    headers: { 'Content-Type': 'application/json'},
                    withCredentials: true
                }
            );
            console.log(response)
            navigate("/");
        } catch (err) {
            console.log(err);
            if (!err?.response) {
                setErrMsg('No Server Response');
            } else if (err.response?.status === 409) {
                setErrMsg('Username taken');
            } else {
                setErrMsg("Registration faild");
            }
            errRef.current.focus();
        };
    };

    return (
        <section>
            <p ref={errRef} className={errMsg ? "text-danger" : 
            "text-primary"} aria-live="assertive">{errMsg}</p>
            <h1>Register</h1>
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
                        <input 
                            className="form-check-input"
                            type="checkbox" 
                            id="is_admin" 
                            name="is_admin" 
                            onChange={handleCheckboxChange}
                        />
                        <label className="form-check-label" htmlFor="is_admin">I'm admin</label>
                    </div>
                    <div>
                        <button className="btn btn-primary">SignUp</button>
                    </div>
                </form>
                <p>
                <span className="line">
                    <Link to="/login">Sign In</Link>
                </span>
                </p>
            </div>
        </section>
    )
}

export default Register