// AuthPage.js

import React, { useState } from "react";
import AuthService from "./AuthService";

function AuthPage({ onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = isLogin
      ? await AuthService.login(username, password)
      : await AuthService.register(username, password);

    if (response.success) {
      onAuthSuccess(username);
    } else {
      alert("Authentication failed!");
    }
  };

  return (
    <div className="auth-container">
      <h2 className="auth-title">{isLogin ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <input
          type="text"
          placeholder="Username"
          value={username}
          className="auth-input"
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          className="auth-input"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="auth-button">
          {isLogin ? "Login" : "Register"}
        </button>
      </form>
      <button onClick={() => setIsLogin(!isLogin)} className="auth-toggle">
        {isLogin ? "Need to register?" : "Already have an account?"}
      </button>
    </div>
  );
}

export default AuthPage;
