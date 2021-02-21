import React, { Component } from 'react';
 
const API = 'http://localhost:5000';
const DEFAULT_QUERY = '/';
 
class App extends Component {
  constructor(props) {
    super(props);
 
    this.state = {
      message: "",
      status_text: "",
      status_code: ""
    };
  }
 
  componentDidMount() {
    fetch(API + DEFAULT_QUERY)
      .then(response => response.json())
      .then(data => this.setState(
        {
          message: data.message,
          status_text: data.status_text,
          status_code: data.status_code
        }));
  }
 
  render() {
    const { message, status_text, status_code } = this.state;
 
    return (
      <div>
      <p>Message: {message}</p>
      <p>Status text: {status_text}</p> 
      <p>Status code: {status_code}.</p>
      </div>
    );
  }
}
 
export default App;