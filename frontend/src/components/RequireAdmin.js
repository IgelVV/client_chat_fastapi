import { useLocation, Outlet, Navigate } from "react-router-dom";
import localAuthName from "../hooks/useAuth";

import {getObjectFromLocalStorage} from "../utils/localStorageManager"


const RequireAdmin = () => {
    const location = useLocation();
    const auth = getObjectFromLocalStorage(localAuthName);

    return (
        auth?.isAdmin
            ?<Outlet />
            :<Navigate to="/login" state={{from: location}} replace />
    )
}

export default RequireAdmin;