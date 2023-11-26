import React from "react";
import { useNavigate } from "react-router-dom";


const Header = function () {

  const navigate = useNavigate();
  const navigateLogin = () => { navigate("/login") };
  const navigateHome = () => { navigate("/") };

  return (
    <div>
      <button type="button" className="btn btn-link" onClick={navigateLogin}>SignIn</button>
      <button type="button" className="btn btn-link" onClick={navigateHome}>Home</button>
    </div>
  );

}

export default Header;