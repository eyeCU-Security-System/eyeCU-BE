import React from "react";
import {Route, Switch} from "react-router-dom";
import Home from "./containers/Home";
import NotFound from "./containers/NotFound";
import Login from "./containers/Login";
import Register from "./containers/Register";

export default function Routes(){
    /**
     * component uses this Switch component from React-Router 
     * that renders the first matching route that is defined within it
     */
    return(
        <Switch>
            <Route exact path="/">
                <Home />
            </Route>
            <Route exact path="/Login">
                <Login />
            </Route>
            <Route exact path="/Register">
                <Register />
            </Route>
            <Route>
                <NotFound />
            </Route>
        </Switch>
    );
}