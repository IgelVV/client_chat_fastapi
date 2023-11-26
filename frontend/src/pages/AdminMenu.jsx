import { useNavigate, } from "react-router-dom";


const AdminMenu = () => {
    const navigate = useNavigate();

    const navigateInbox = () => { navigate("/inbox"); }
    const navigateMy = () => { navigate("/my"); }
    const navigateAll = () => { navigate("/all"); }


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