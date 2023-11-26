import { createContext, useState } from "react";
import { getObjectFromLocalStorage } from "../utils/localStorageManager";
import localAuthName from "../hooks/useAuth";


const AuthContext = createContext({})

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState({});

    return (
        <AuthContext.Provider value={{auth, setAuth}} >
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContext

export const getLocalAuth = () => {
    return(getObjectFromLocalStorage(localAuthName))
}