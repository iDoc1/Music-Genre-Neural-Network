import React from 'react';
import { Form, Button } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';


function SearchBox({ onClickSubmit }) {

    return (
        <>
            <Form>
            <Form.Group className="youtubeSearchBox" controlId="formYoutubeSearch">
                <Form.Label>Enter the name of song to test</Form.Label>
                <Form.Control type="text" placeholder="Enter song name" />
                <Form.Text className="text-muted">
                Press Submit to search for a song on YouTube to test to model on
                </Form.Text>
            </Form.Group>

            <Button className ="submitButton" variant="primary" type="submit" onClick={() => onClickSubmit('american idiot')}>
                Submit
            </Button>
            </Form>
        </>
    );
}

export default SearchBox;
