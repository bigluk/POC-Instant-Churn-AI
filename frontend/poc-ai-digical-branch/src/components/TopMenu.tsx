import "../styles/layout.css";
import { Navbar, Container, Nav } from "react-bootstrap";
import { FaUser, FaDesktop, FaUniversity, FaBrain, FaKey } from 'react-icons/fa';

const TopMenu = () => {
    return (
        <Navbar expand="lg" style={{ backgroundColor: '#007a33' }} variant="dark">
            <Container>
                {/* Logo */}
                <Navbar.Brand href="/">
                    <span style={{ fontWeight: 'bold', color: 'white' }}>Digical</span>
                    <span style={{ color: '#c0c0c0' }}> ABC</span>
                </Navbar.Brand>

                <Navbar.Toggle aria-controls="basic-navbar-nav" />

                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="ms-auto align-items-center">
                        <Nav.Link href="#"><FaBrain /> Investment Propensity</Nav.Link>
                        <Nav.Link href="#"><FaUser /> Admin Admin</Nav.Link>
                        <Nav.Link href="#"><FaKey /></Nav.Link>
                        <Nav.Link href="#"><FaUniversity /> 10000</Nav.Link>
                        <Nav.Link href="#"><FaDesktop /> ENG</Nav.Link>
                        <Nav.Link href="#">ENG</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default TopMenu;
