import React from 'react';

import Header from './components/Header';
import Home from './pages/Home';
import Register from './pages/Register';
import Counter from './components/Counter';
import Login from './pages/Login';
import AdminMenu from './pages/AdminMenu';
import AllChats from './pages/AllChats';
import MyChats from './pages/MyChats';
import Inbox from './pages/Inbox';
import Chat from './pages/Chat';
import User from './pages/User';


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
            element={<User />}
          />
          <Route
            exact
            path="/chat/:id"
            element={<Chat />}
          />
        </Route>
        <Route element={<RequireAdmin />}>
          <Route
            exact
            path="/admin"
            element={<AdminMenu />}
          />
          <Route
            exact
            path="/all"
            element={<AllChats />}
          />
          <Route
            exact
            path="/my"
            element={<MyChats />}
          />
          <Route
            exact
            path="/inbox"
            element={<Inbox />}
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
    </main>
  );
}

export default App;
