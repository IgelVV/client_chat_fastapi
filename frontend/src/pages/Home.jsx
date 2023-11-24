import { useRef, useState, useEffect } from "react";
import useAuth from "../hooks/useAuth";
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css'


const Home = () => {
    const { auth } = useAuth();
    const navigate = useNavigate();
    console.log("home")
    console.log(auth)
    useEffect(
        ()=> {
            console.log("home")
            console.log(auth)
            if (auth?.isAdmin) {
                navigate("/admin")
            } else {

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