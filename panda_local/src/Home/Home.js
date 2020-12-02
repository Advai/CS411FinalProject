import React, { Component } from "react";
import { Button } from 'react-bootstrap';
import history from './../history';
import "./Home.css";
import withListLoading from './../components/WithListLoading';
import List from './../components/List';
import axios from 'axios';
import WithListLoading from "./../components/WithListLoading";
export default class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: true,
            repos: null,
            playerTag: "",
        }
        this.ListLoading = withListLoading(List);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
    }
    ListLoading = withListLoading(List);
    handleSearch(event) {
        let headers = new Headers();

        headers.append('Content-Type', 'application/json');
        headers.append('Accept', 'application/json');
        headers.append('Origin','http://localhost:5000');
        var self = this;
        axios({
            url: "/search",
            baseURL: 'http://127.0.0.1:5000',
            method: 'POST',
            headers: headers,
            data: {
                tag: this.state.playerTag
            },
        })
            .then(function (response) {
                console.log(response.data);
                const allPlacings = response.data;
                
                self.setState({ loading : false, repos: allPlacings});
            })
            .catch(function (error) {
                console.log(error);
            })
            .then(function () {
                // always executed
                console.log("I always run");
            });
    }
    
    handleInputChange(event) {
        const {value, name} = event.target;
        this.setState({
            [name]: value
        });
    };

    render() {
    return (
        <div className="Home">
        <div className="lander">
            <h1>Home page</h1>
            <p>Search for a Smash Player</p>
            <form>
            <input type='text' name ='playerTag' placeholder='player tag' value={this.state.playerTag} onChange={this.handleInputChange}/>
            <Button variant="btn btn-success" onClick={this.handleSearch}>Submit</Button>
            </form>
        </div>
        <div>
        <this.ListLoading isLoading={this.state.loading} repos={this.state.repos}/>
        </div>
        </div>
    );
    }
}