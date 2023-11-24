import { useLocation, Outlet, Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import localAuthName from "../hooks/useAuth";

import {getObjectFromLocalStorage} from "../utils/localStorageManager"


const RequireAuth = () => {
    // const { auth } = useAuth();
    const location = useLocation();
    const auth = getObjectFromLocalStorage(localAuthName);

    return (
        auth?.username
            ?<Outlet />
            :<Navigate to="/login" state={{from: location}} replace />
    )
}

export default RequireAuth;