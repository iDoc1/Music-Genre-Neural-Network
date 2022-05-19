import React from 'react';
import { Form, Button } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';


function SearchBox() {

    return (
        <>
            <Form>
            <Form.Group className="youtubeSearchBox" controlId="formYoutubeSearch">
                <Form.Label>Enter the name of song you would like to test</Form.Label>
                <Form.Control type="text" placeholder="Enter song name" />
                <Form.Text className="text-muted">
                Press Submit to view a list of YouTube videos to test the model on
                </Form.Text>
            </Form.Group>

            <Button className ="submitButton" variant="primary" type="submit">
                Submit
            </Button>
            </Form>
        </>
    );
}

export default SearchBox;
