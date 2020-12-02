import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";
import history from './history';
import Home from "./Home/Home";
import HeadToHead from "./HeadToHead/HeadToHead"
import Tournaments from "./Tournaments/Tournaments"
import Elo from "./components/Elo";
import InsertPlayer from "./components/InsertPlayer";
import DeletePlayer from "./components/DeletePlayer";
import UpdatePlayer from "./components/UpdatePlayer";
// https://rookiecoder.medium.com/react-button-click-navigate-to-new-page-6af7397ea220
export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/HeadToHead" exact component={HeadToHead} />
                    <Route path="/Elo" exact component={Elo}/>
                    <Route path="/insert" exact component={InsertPlayer} />
                    <Route path='/delete' exact component={DeletePlayer} />
                    <Route path='/update' exact component={UpdatePlayer} />
                    {/* <Route path="/Contact" component={Contact} /> */}
                    {/* <Route path="/Products" component={Products} /> */}
                </Switch>
            </Router>
        )
    }
}