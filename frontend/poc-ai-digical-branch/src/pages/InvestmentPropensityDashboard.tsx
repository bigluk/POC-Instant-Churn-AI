import React, { useState, useEffect } from "react";
import { Container, Table, Form, Button, Modal } from "react-bootstrap";
import { FaCheck, FaTimes } from "react-icons/fa";
import type { User } from "../types/User";
import { Link } from "react-router-dom";
import UserChart from "../components/UserChart";

interface SortConfig {
    key: keyof User | null;
    direction: "asc" | "desc";
}

interface FilterConfig {
    min: string;
    max: string;
}

const UserTable: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [allUsers, setAllUsers] = useState<User[]>([]);
    const [sortConfig, setSortConfig] = useState<SortConfig>({ key: null, direction: "asc" });
    const [filter, setFilter] = useState<FilterConfig>({ min: "", max: "" });
    const [loading, setLoading] = useState(true);
    const [chartData, setChartData] = useState<any[]>([]);
    const [selectedUser, setSelectedUser] = useState<string | null>(null);
    const [showChartModal, setShowChartModal] = useState(false);


    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const res = await fetch("/api/fetch-users");
                const data = await res.json();

                setUsers(data);
                setAllUsers(data);
            } catch (error) {
                console.error("Error during users fetching:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();
    }, []);

    const sortData = (key: keyof User) => {
        let direction: "asc" | "desc" = "asc";
        if (sortConfig.key === key && sortConfig.direction === "asc") {
            direction = "desc";
        }

        const sorted = [...users].sort((a, b) => {
            if (typeof a[key] === "number") {
                return direction === "asc"
                    ? (a[key] as number) - (b[key] as number)
                    : (b[key] as number) - (a[key] as number);
            }
            return direction === "asc"
                ? String(a[key]).localeCompare(String(b[key]))
                : String(b[key]).localeCompare(String(a[key]));
        });

        setSortConfig({ key, direction });
        setUsers(sorted);
    };

    const applyFilter = () => {
        const min = filter.min ? parseInt(filter.min, 10) : 0;
        const max = filter.max ? parseInt(filter.max, 10) : 100;

        const filtered = allUsers.filter(
            (user) => user.investment_propensity >= min && user.investment_propensity <= max
        );

        setUsers(filtered);
    };

    const resetFilter = () => {
        setFilter({ min: "", max: "" });
        setUsers(allUsers);
    };

    const handleRowClick = async (userId: string) => {
        setSelectedUser(userId);
        try {
            const res = await fetch(`/api/chart/${userId}`);
            const data = await res.json();
            setChartData(data);
            setShowChartModal(true);
        } catch (err) {
            console.error("Errore caricamento grafico", err);
        }
    };


    if (loading) return <Container className="mt-2">Loading...</Container>;

    return (
        <Container className="mt-4">
            <h2>User List</h2>

            <Form className="mb-3 d-flex align-items-end gap-2">
                <Form.Group>
                    <Form.Label>Min IP (%)</Form.Label>
                    <Form.Control
                        type="number"
                        value={filter.min}
                        onChange={(e) => setFilter({ ...filter, min: e.target.value })}
                    />
                </Form.Group>

                <Form.Group>
                    <Form.Label>Max IP (%)</Form.Label>
                    <Form.Control
                        type="number"
                        value={filter.max}
                        onChange={(e) => setFilter({ ...filter, max: e.target.value })}
                    />
                </Form.Group>

                <Button variant="success" onClick={applyFilter}>Apply Filter</Button>
                <Button variant="secondary" onClick={resetFilter}>Reset</Button>
            </Form>

            <Table bordered hover>
                <thead>
                    <tr>
                        <th onClick={() => sortData("id")}>ID</th>
                        <th onClick={() => sortData("first_name")}>First Name</th>
                        <th onClick={() => sortData("last_name")}>Last Name</th>
                        <th>Age</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Balance</th>
                        <th onClick={() => sortData("investment_propensity")}>Investment Propensity (IP)</th>
                        <th>Inclined to Invest</th>
                    </tr>
                </thead>

                <tbody>
                    {users.map((u, index) => (
                        <tr
                            key={u.id}
                            className={index % 2 !== 0 ? "green-row" : ""}
                            style={{ cursor: "pointer" }}
                            onClick={() => handleRowClick(u.id)}
                        >
                            <td>
                                <Link
                                    to={`/dashboard/${u.id}`}
                                    style={{ color: "#0d6efd", textDecoration: "underline", fontWeight: 600 }}
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    {u.id}
                                </Link>
                            </td>
                            <td>{u.first_name}</td>
                            <td>{u.last_name}</td>
                            <td>{u.age}</td>
                            <td>{u.phone_number}</td>
                            <td>{u.email}</td>
                            <td>{u.balance}</td>
                            <td>{u.investment_propensity}%</td>
                            <td>{u.prediction === 1 ? <FaCheck color="green" /> : <FaTimes color="red" />}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Modal
                show={showChartModal}
                onHide={() => setShowChartModal(false)}
                size="xl"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title>Investment Propensity Trend for User {selectedUser}</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <UserChart data={chartData} userId={selectedUser!} />
                </Modal.Body>
            </Modal>


        </Container>
    );
};

export default UserTable;
