import React, { Component } from "react";
import { useState, setState } from 'react'
import { Button } from 'react-bootstrap';
import history from './../history';
import withListLoading from './../components/WithListLoading';
import EloList from './../components/EloList';
import axios from 'axios';
import PGRList from "./../components/PGRList";
import WithListLoading from "./../components/WithListLoading";
import styles from "./../components/HeadToHeadList.module.css"
export default class Elo extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            loading2: true,
            plr_repos: null,
            pgr_repos: null,
        }
        // make new ELO List componenet
        this.PLRListLoading = withListLoading(EloList);
        this.PGRListLoading = withListLoading(PGRList);
        this.handlePLR = this.handlePLR.bind(this);
        this.handlePGR = this.handlePGR.bind(this);
    }
    // query for elo
    handlePLR(event) {
        let headers = new Headers();

        headers.append('Content-Type', 'application/json');
        headers.append('Accept', 'application/json');
        headers.append('Origin','http://localhost:5000');
        var self = this;
        axios({
            url: "/plr",
            baseURL: 'http://127.0.0.1:5000',
            method: 'POST',
            headers: headers,
        })
            .then(function (response) {
                console.log(response.data);
                const allPlacings = response.data;
                
                self.setState({ loading : false, plr_repos: allPlacings});
            })
            .catch(function (error) {
                console.log(error);
            })
            .then(function () {
                // always executed
                console.log("I always run");
            });
    }

    handlePGR(event) {
        let headers = new Headers();

        headers.append('Content-Type', 'application/json');
        headers.append('Accept', 'application/json');
        headers.append('Origin','http://localhost:5000');
        var self = this;
        axios({
            url: "/pgr",
            baseURL: 'http://127.0.0.1:5000',
            method: 'POST',
            headers: headers,
        })
            .then(function (response) {
                console.log(response.data);
                const allPlacings = response.data;
                
                self.setState({ loading2 : false, pgr_repos: allPlacings});
            })
            .catch(function (error) {
                console.log(error);
            })
            .then(function () {
                // always executed
                console.log("I always run");
            });
    }

    componentDidMount(){
        this.handlePLR();
        this.handlePGR();
    }

    render() {
    return (
        <div className={styles.div}>
        <div className="lander">
            <h1>Panda Local Rankings vs PGRU</h1>
            {/* <p>Search for a Smash Player</p> */}
            {/* <form>
            <input type='text' name ='playerTag' placeholder='player tag' value={this.state.playerTag} onChange={this.handleInputChange}/>
            <Button variant="btn btn-success" onClick={this.handleSearch}>Submit</Button>
            </form> */}
        </div>
        <div key="div1">
        <this.PLRListLoading isLoading={this.state.loading} repos={this.state.plr_repos}/>
        <this.PGRListLoading isLoading={this.state.loading2} resp={this.state.pgr_repos}/>
        </div>
        </div>
    );
    }
}