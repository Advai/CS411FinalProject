import React from 'react';
import './Navbar.css';
import { Navbar, Nav, Form, Button, NavDropdown, FormControl } from 'react-bootstrap';
import { withRouter } from 'react-router-dom';

const Navigation = (props) => {
    console.log(props);
    return (
        <Navbar bg="light" expand="lg">
        <Navbar.Brand href="/">Panda Local</Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse>
          <Nav className="mr-auto">
          <Nav.Link href="/Elo">Rankings</Nav.Link>
            <Nav.Link href="/HeadToHead">Head to Head</Nav.Link>
            <Nav.Link href="/insert">Insert Player</Nav.Link>
            <Nav.Link href="/delete">Delete Player</Nav.Link>
            <Nav.Link href="/update">Update Player</Nav.Link>
            {/* <NavDropdown title="Games">
              <NavDropdown.Item href="#action/1">Melee</NavDropdown.Item>
              <NavDropdown.Item href="#action/2">Ultimate</NavDropdown.Item>
            </NavDropdown> */}
          </Nav>
          {/* <Form inline>
            <FormControl type="text" placeholder="search" className="mr-sm-2" />
            <Button variant="outline-primary">search</Button>
          </Form> */}
        </Navbar.Collapse>
      </Navbar>
        // <Navbar bg="primary" variant="dark">
        //     <Navbar.Brand href="#home">React Button</Navbar.Brand>
        //     <Navbar.Toggle aria-controls="basic-navbar-nav" />
        //     <Navbar.Collapse id="basic-navbar-nav">
        //         <Nav className="mr-auto">
        //             <Nav.Link href="/">Home</Nav.Link>
        //             <Nav.Link href="/About">About</Nav.Link>
        //             <Nav.Link href="/Contact">Contact</Nav.Link>
        //             <Nav.Link href="/Products">Products</Nav.Link>
        //         </Nav>
        //     </Navbar.Collapse>
        // </Navbar>
    )
}

export default withRouter(Navigation);