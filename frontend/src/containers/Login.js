import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./Login.css";

export default function Login(){
    const[username, setUsername] = useState("");
    const[password, setPassword] = useState("");
    const[firstName, setFirstName] = useState("");
    const[lastName, setLastName] = useState("");

    function validateForm(){
        return username.length > 0 && 
                password.length > 0 &&
                firstName.length > 0 &&
                lastName.length > 0;

    }

    function handleSubmit(event){
        event.preventDefault();
    }

    return(
        <div className="Login">
            <Form onSubmit={handleSubmit}>
                <Form.Group size="lg" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        autoFocus
                        type="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}/>
                </Form.Group>

                <Form.Group size="lg" controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        autoFocus
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}/>
                </Form.Group>
                <Button block size="sm" type = "submit" disabled={!validateForm()}>
                    Login
                </Button>
            </Form>
        </div>
    )




}