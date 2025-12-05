import React, { useContext, useEffect, useState } from "react";
import { Container, Row, Col, Card } from "react-bootstrap";
import { useParams } from "react-router-dom";
import { BsCalendar3, BsDot } from "react-icons/bs";
import aiIcon from '../assets/ai-model.png';
import type { User } from "../types/User";
import { UserContext } from "../context/UserContext";

// Customer Data Component
export const InvestmentPropensity: React.FC = () => {
    const user = useContext(UserContext);
    return (
        <div>
            <h5>Propensity to invest</h5>
            <Card className="mb-3 p-3 shadow-sm text-center" style={{ minHeight: "160px" }}>
                <div className="mt-3 d-flex justify-content-center">
                    <img src={aiIcon} alt="Investment Propensity Model" className="img-fluid" style={{ height: "60px" }} />
                </div>
                <div className="mt-3">
                    <strong>{user?.investmentPropensity}%</strong>
                </div>
            </Card>
        </div>
    );
};

// Customer Data Component
export const CustomerData: React.FC = () => {
    const { userId } = useParams();
    return (
        <div>
            <h5>Customer data</h5>
            <Card className="mb-3 p-3 shadow-sm" style={{ minHeight: "160px" }}>
                <Row className="mt-2">
                    <Col md={3}><strong>Customer ID</strong><div>{userId}</div></Col>
                    <Col md={3}><strong>Branch name</strong><div>33300</div></Col>
                    <Col md={3}><strong>Segment</strong><div>MASS</div></Col>
                    <Col md={3}><strong>Sub‑Segment</strong><div>—</div></Col>
                </Row>
                <Row className="mt-3">
                    <Col md={3}><strong>Risk rating</strong><div>—</div></Col>
                    <Col md={6}><strong>Relationship Manager</strong><div>Ing. Oto Kosár</div></Col>
                </Row>
            </Card>
        </div>
    );
};

// Next Meeting Component
export const NextMeeting: React.FC = () => {
    return (
        <div>
            <h5>Next meeting</h5>
            <Card className="mb-3 p-3 shadow-sm text-center" style={{ minHeight: "160px" }}>
                <div className="d-flex justify-content-center">
                    <BsCalendar3 size={30} style={{ color: "black" }} />
                </div>
                <div className="mt-3 mb-1 text-muted">No meeting planned.</div>
                <small>Plan a meeting with your client to open his new bank account.</small>
            </Card>
        </div>
    );
};

// Customer History Component
export const CustomerHistory: React.FC = () => {
    return (
        <div>
            <h5>Customer History</h5>
            <Card className="mb-3 p-3 shadow-sm text-center" style={{ minHeight: "160px" }}>
                <div className="mt-4 text-muted">No data available</div>
            </Card>
        </div>
    );
};

// Balance Component
export const Balance: React.FC = () => {
    return (
        <div>            <h5>Balance</h5>

            <Card className="mb-3 p-3 shadow-sm" style={{ minHeight: "200px" }}>
                <Row className="mt-3">
                    <Col md={6}>
                        <h5>ASSETS</h5>
                        <BsDot size={40} style={{ color: "rgba(81, 102, 223, 1)" }} />100% accounts
                        <div>Total asset: 82.351,65 EUR</div>
                    </Col>
                    <Col md={6}>
                        <h5>LIABILITY</h5>
                        <div>
                            <BsDot size={40} style={{ color: "rgba(255, 120, 120, 1)" }} />0% credit cards
                        </div>
                        <div>
                            <BsDot size={40} style={{ color: "rgba(107, 23, 23, 1)" }} />0% loans
                        </div>
                        <div>
                            <BsDot size={40} style={{ color: "rgba(216, 24, 24, 1)" }} />0% accounts
                        </div>
                        <div>Total liability: 0,00 EUR</div>
                    </Col>
                </Row>
            </Card>
        </div>
    );
};

// Profitability Component
export const Profitability: React.FC = () => (
    <div>
        <h5>Profitability</h5>
        <Card className="mb-3 p-3 shadow-sm text-center" style={{ minHeight: "200px" }}>
            <div className="mt-4 text-muted">No data available</div>
        </Card>
    </div>
);

// Pending Monitor Component
export const PendingMonitor: React.FC = () => (
    <div>
        <h5>Pending Monitor</h5>
        <Card className="mb-3 p-3 shadow-sm text-center" style={{ minHeight: "200px" }}>
            <div className="mt-4 text-muted">The customer has not pending process yet.</div>
        </Card>
    </div>
);


// Main Page Component
const CustomerDashboard: React.FC = () => {
    const { userId } = useParams();
    const [user, setUser] = useState<User>();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUserById = async () => {
            const res = await fetch(`/api/fetch-user/${userId}`);
            const data = await res.json();
            setUser(data);
            setLoading(false);
        };

        fetchUserById();
    }, []);

    if (loading) return <div>Loading...</div>;

    return (
        <UserContext.Provider value={user}>
            <Container className="mt-4">
                <h3 className="mb-4">
                    {user?.firstName} {user?.lastName}
                </h3>

                <Row>
                    <Col md={6}><CustomerData /></Col>
                    <Col md={2}><NextMeeting /></Col>
                    <Col md={2}><CustomerHistory /></Col>
                    <Col md={2}><InvestmentPropensity /></Col>
                </Row>

                <Row>
                    <Col md={6}><Balance /></Col>
                    <Col md={3}><Profitability /></Col>
                    <Col md={3}><PendingMonitor /></Col>
                </Row>
            </Container>
        </UserContext.Provider>
    );
};

export default CustomerDashboard;