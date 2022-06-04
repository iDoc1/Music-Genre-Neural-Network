import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';


function TopNavbar() {
    
    return (
        <>
            <Navbar bg='primary' variant='dark'>
                <Container>
                <Navbar.Brand href='/'>Music Genre Classifier</Navbar.Brand>
                <Nav className='me-auto'>
                <Nav.Link href='/'>Model Accuracy Tester</Nav.Link>
                <Nav.Link href='/about'>About this Project</Nav.Link>
                </Nav>
                </Container>
            </Navbar>
        </>
    );
}

export default TopNavbar;
