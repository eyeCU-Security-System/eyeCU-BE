import './App.css';
import React from 'react';
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Routes from './Routes';
import { LinkContainer} from "react-router-bootstrap";
import { Link } from 'react-router-dom';
//useState used for state variable that contains data retrieved from backend
//useEffect used to retrive data from backend


function App() {
  /*
  const [data, setData] = useState([{}]);

  useEffect(() => {
    fetch("/accounts")
    .then(res => res.json())
    .then(data => {
      setData(data)
      console.log(data)
    })
  }, []);
*/
  
  return (
    <div className="App container py-3">
      <Navbar collapseOnSelect bg="dark" expand="md" className="mb-3">
        <Navbar.Brand className = "font-weight-bold text-muted">
        <LinkContainer to ="/">
        <Nav.Link className="HomeLogo">eyeCU</Nav.Link>
        </LinkContainer>
        </Navbar.Brand>
        <Navbar.Toggle  />
        <Navbar.Collapse className='justify-content-end'>
          <Nav activeKey = {window.location.pathname}>
            <LinkContainer to ="/Login">
              <Nav.Link>Login</Nav.Link>
              </LinkContainer>
              <LinkContainer to ="Register">
            <Nav.Link>Register</Nav.Link>
            </LinkContainer>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <Routes />
    </div>
  );
}

export default App;
