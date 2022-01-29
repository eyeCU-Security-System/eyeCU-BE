import React, { useState } from "react";
/*
import Form from "react-bootstrap/Form";
import { useHistory } from "react-router-dom";
import LoaderButton from "../components/LoaderButton";
import { useAppContext } from "../lib/contextLib";
import { useFormFields } from "../lib/hooksLib";
import { onError } from "../lib/errorLib";
import "./Register.css";

export default function Register(){
    /*
    const[fields, handleFieldChange] = useFormFields({
        username: "",
        password: "",
        confirmPassword: "",
        firstName: "",
        lastName: "",
    });

    const history = useHistory();
    const [newUser, setNewUser] = useState(null);
    const { userHasAuthenticated } = useAppContext();
    const [isLoading, setIsLoading] = useState(false);



    function validateForm(){
        return(
            fields.username.length > 0 &&
            fields.password.length > 0 &&
            fields.password === fields.confirmPassword &&
            fields.firstName.length > 0 &&
            fields.lastName.length > 0
        );
    }

    function validateConfirmationForm() {
        return fields.confirmationCode.length > 0;
      }
    
    

    function renderConfirmationForm() {
        return (
          <Form onSubmit={handleConfirmationSubmit}>
            <Form.Group controlId="confirmationCode" size="lg">
              <Form.Label>Confirmation Code</Form.Label>
              <Form.Control
                autoFocus
                type="tel"
                onChange={handleFieldChange}
                value={fields.confirmationCode}
              />
              <Form.Text muted>Please check your email for the code.</Form.Text>
            </Form.Group>
            <LoaderButton
              block
              size="lg"
              type="submit"
              variant="success"
              isLoading={isLoading}
              disabled={!validateConfirmationForm()}
            >
              Verify
            </LoaderButton>
          </Form>
        );
      }

    async function handleConfirmationSubmit(event) {
       event.preventDefault();
       setIsLoading(true);
    }

    function renderForm() {
        return (
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="username" size="lg">
              <Form.Label>Username</Form.Label>
              <Form.Control
                autoFocus
                type="username"
                value={fields.username}
                onChange={handleFieldChange}
              />
            </Form.Group>
            <Form.Group controlId="password" size="lg">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                value={fields.password}
                onChange={handleFieldChange}
              />
            </Form.Group>
            <Form.Group controlId="confirmPassword" size="lg">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                type="password"
                onChange={handleFieldChange}
                value={fields.confirmPassword}
              />
            </Form.Group>
            <Form.Group controlId="firstName" size="lg">
              <Form.Label>First Name</Form.Label>
              <Form.Control
                type="firstName"
                onChange={handleFieldChange}
              />
            </Form.Group>
            <Form.Group controlId="lastName" size="lg">
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                type="lastName"
                onChange={handleFieldChange}
              />
            </Form.Group>
            <LoaderButton
              block
              size="sm"
              type="submit"
              variant="success"
              isLoading={isLoading}
              disabled={!validateForm()}
            >
              Signup
            </LoaderButton>
          </Form>
        );
      }

    



    return(
        <div className="Register">
            {newUser==null? renderForm(): renderConfirmationForm()}

        </div>
    );


}

*/
