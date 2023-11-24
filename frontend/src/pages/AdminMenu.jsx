import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "../api/axios";

const USERS_URL = '/'


const AdminMenu = () => {
    const [users, setUsers] = useState();
    const axiosPrivate = axios
    const navigate = useNavigate();
    const location = useLocation();

    const navigateInbox = () =>{navigate("/users");}
    const navigateMy = () =>{navigate("/counter");}
    const navigateAll = () =>{navigate("/counter");}
    

    return (
        <section>
            <h1>Admin menu</h1>
            <button className="btn btn-info" onClick={navigateInbox}>
                Inbox
            </button>
            <button className="btn btn-light" onClick={navigateMy}>
                My
            </button>
            <button className="btn btn-dark" onClick={navigateAll}>
                All
            </button>
        </section>
    );
};
    
export default AdminMenu;