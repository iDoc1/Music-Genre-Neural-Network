import React from 'react';
import { useState } from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';


function TopNavbar() {
    const [activeKey, setActiveKey] = useState(1)

    return (
        <>

            <Navbar bg="primary" variant="dark">
                <Container>
                <Navbar.Brand href="#home">Music Genre Classifier</Navbar.Brand>
                <Nav className="me-auto">
                <Nav.Link href="#home">Model Accuracy Tester</Nav.Link>
                <Nav.Link href="#features">About this Project</Nav.Link>
                </Nav>
                </Container>
            </Navbar>

        </>
    );
}

export default TopNavbar;
