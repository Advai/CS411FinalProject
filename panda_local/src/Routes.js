import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";
import history from './history';
import Home from "./Home/Home";
import HeadToHead from "./HeadToHead/HeadToHead"
import Tournaments from "./Tournaments/Tournaments"
// https://rookiecoder.medium.com/react-button-click-navigate-to-new-page-6af7397ea220
export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/Tournaments" exact component={Tournaments} />
                    <Route path="/HeadToHead" exact component={HeadToHead} />
                    {/* <Route path="/Contact" component={Contact} /> */}
                    {/* <Route path="/Products" component={Products} /> */}
                </Switch>
            </Router>
        )
    }
}