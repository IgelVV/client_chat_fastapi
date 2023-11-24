import React from 'react';

import Header from './components/Header';
import Home from './pages/Home';
import Register from './pages/Register';
import Counter from './components/Counter';
import Login from './pages/Login';
import Users from './components/Users';
import AdminMenu from './pages/AdminMenu';

import RequireAuth from './components/RequireAuth';
import RequireAdmin from './components/RequireAdmin';

import { Routes, Route } from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.css'

function App() {
  return (
    <main className="App">
      <Header />
        <Routes>
            <Route element={<RequireAuth />}>
              <Route
                exact
                path="/"
                element={<Home />}
              />
              <Route
                exact
                path="/user"
                element={<Counter />}
              />
            </Route>
            <Route element={<RequireAdmin />}>
              <Route
                exact
                path="/users"
                element={<Users />}
              />
              <Route
                exact
                path="/admin"
                element={<AdminMenu />}
              />
            </Route>
            <Route
                exact
                path="/counter"
                element={<Counter />}
            />
            <Route
              path="/register"
              element={<Register />}
            />
            <Route
              path="/login"
              element={<Login />}
            />
        </Routes>
        {/* <Header/> */}
    </main>
  );
}

export default App;
