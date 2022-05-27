import React from 'react';
import { useState } from 'react';
import { Form, Button } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';


function SearchBox({ fetchSearchData }) {
    const [songInput, setSongInput] = useState('');

    // Prevents default POST request then executes function to show thumbnails
    const onFormSubmit = (e) => {
        e.preventDefault();
        fetchSearchData(songInput);
    }

    return (
        <>
            <Form onSubmit={onFormSubmit}>
            <Form.Group className="youtubeSearchBox" controlId="formYoutubeSearch">
                <Form.Label>Enter the name of song to test</Form.Label>
                <Form.Control 
                    type="text" 
                    placeholder="Enter song name"
                    onChange={e => setSongInput(e.target.value)}/>
                <Form.Text className="text-muted">
                Press Submit to search for a song on YouTube to test to model on
                </Form.Text>
            </Form.Group>

            <Button 
                className ="submitButton" 
                variant="primary" 
                type="submit" 
                >
                Submit
            </Button>
            </Form>
        </>
    );
}

export default SearchBox;
