import { useEffect } from "react";
import { useNavigate } from 'react-router-dom';

import { getObjectFromLocalStorage } from "../utils/localStorageManager";
import localAuthName from "../hooks/useAuth";


const Home = () => {
    const auth = getObjectFromLocalStorage(localAuthName);
    const navigate = useNavigate();

    useEffect(
        () => {
            if (auth?.isAdmin) {
                navigate("/admin")
            } else {
                console.log("redirect from Home")
                navigate("/user")
            }
        }
    )

    return (
        <section>
        </section>
    )
}
export default Home