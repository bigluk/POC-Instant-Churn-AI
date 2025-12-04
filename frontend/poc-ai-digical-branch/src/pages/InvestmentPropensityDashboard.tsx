import React, { useState } from "react";
import { Container, Table, Form, Button } from "react-bootstrap";

// Define User type
interface User {
    id: string
    firstName: string;
    lastName: string;
    birthDate: string;
    age: number;
    investmentPropensity: number; // numeric for sorting/filtering
    phone: string;
    email: string;
}

// Sorting configuration type
interface SortConfig {
    key: keyof User | null;
    direction: "asc" | "desc";
}

// Filter type
interface FilterConfig {
    min: string;
    max: string;
}

// Sample data
const initialUsers: User[] = [
    { id: "658238", firstName: "John", lastName: "Doe", birthDate: "15-05-1990", age: 33, investmentPropensity: 45, phone: "+1 555-1234", email: "john.doe@example.com" },
    { id: "909098", firstName: "Emma", lastName: "Smith", birthDate: "30-09-1985", age: 38, investmentPropensity: 70, phone: "+1 555-5678", email: "emma.smith@example.com" },
    { id: "732781", firstName: "Michael", lastName: "Johnson", birthDate: "12-01-2000", age: 23, investmentPropensity: 55, phone: "+1 555-9012", email: "michael.johnson@example.com" },
    { id: "451239", firstName: "Sophia", lastName: "Brown", birthDate: "22-07-1992", age: 31, investmentPropensity: 60, phone: "+1 555-2345", email: "sophia.brown@example.com" },
    { id: "672314", firstName: "Liam", lastName: "Davis", birthDate: "03-03-1988", age: 35, investmentPropensity: 50, phone: "+1 555-6789", email: "liam.davis@example.com" },
    { id: "984321", firstName: "Olivia", lastName: "Martinez", birthDate: "14-11-1995", age: 28, investmentPropensity: 75, phone: "+1 555-3456", email: "olivia.martinez@example.com" },
    { id: "120987", firstName: "Noah", lastName: "Garcia", birthDate: "25-02-1999", age: 24, investmentPropensity: 65, phone: "+1 555-7890", email: "noah.garcia@example.com" },
    { id: "876543", firstName: "Ava", lastName: "Wilson", birthDate: "18-08-1987", age: 36, investmentPropensity: 40, phone: "+1 555-0123", email: "ava.wilson@example.com" },
    { id: "334455", firstName: "Ethan", lastName: "Anderson", birthDate: "09-06-2001", age: 22, investmentPropensity: 55, phone: "+1 555-4567", email: "ethan.anderson@example.com" }
];

const UserTable: React.FC = () => {
    const [users, setUsers] = useState<User[]>(initialUsers);
    const [sortConfig, setSortConfig] = useState<SortConfig>({ key: null, direction: "asc" });
    const [filter, setFilter] = useState<FilterConfig>({ min: "", max: "" });

    // Sorting function
    const sortData = (key: keyof User) => {
        let direction: "asc" | "desc" = "asc";
        if (sortConfig.key === key && sortConfig.direction === "asc") {
            direction = "desc";
        }
        setSortConfig({ key, direction });

        const sorted = [...users].sort((a, b) => {
            if (key === "investmentPropensity" || key === "age") {
                return direction === "asc" ? a[key] - b[key] : b[key] - a[key];
            } else {
                return direction === "asc"
                    ? String(a[key]).localeCompare(String(b[key]))
                    : String(b[key]).localeCompare(String(a[key]));
            }
        });

        setUsers(sorted);
    };

    // Filter function
    const applyFilter = () => {
        const min = filter.min ? parseInt(filter.min, 10) : 0;
        const max = filter.max ? parseInt(filter.max, 10) : 100;
        const filtered = initialUsers.filter(
            (user) => user.investmentPropensity >= min && user.investmentPropensity <= max
        );
        setUsers(filtered);
    };

    const resetFilter = () => {
        setFilter({ min: "", max: "" });
        setUsers(initialUsers);
    };

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

                <Button variant="success" onClick={applyFilter}>
                    Apply Filter
                </Button>
                <Button variant="secondary" onClick={resetFilter}>
                    Reset
                </Button>
            </Form>

            <Table bordered hover>
                <thead>
                    <tr>
                        <th onClick={() => sortData("id")} style={{ cursor: "pointer" }}>
                            Customer ID {sortConfig.key === "id" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
                        </th>
                        <th onClick={() => sortData("firstName")} style={{ cursor: "pointer" }}>
                            First Name {sortConfig.key === "firstName" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
                        </th>
                        <th onClick={() => sortData("lastName")} style={{ cursor: "pointer" }}>
                            Last Name {sortConfig.key === "lastName" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
                        </th>
                        <th>Birth Date</th>
                        <th onClick={() => sortData("age")} style={{ cursor: "pointer" }}>
                            Age {sortConfig.key === "age" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
                        </th>
                        <th>Phone Number</th>
                        <th onClick={() => sortData("email")} style={{ cursor: "pointer" }}>
                            Email {sortConfig.key === "email" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
                        </th>
                        <th onClick={() => sortData("investmentPropensity")} style={{ cursor: "pointer" }}>
                            Investment Propensity (IP) {sortConfig.key === "investmentPropensity" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user, index) => (
                        <tr className={index % 2 !== 0 ? 'green-row' : ''} key={index}>
                            <td>{user.id}</td>
                            <td>{user.firstName}</td>
                            <td>{user.lastName}</td>
                            <td>{user.birthDate}</td>
                            <td>{user.age}</td>
                            <td>{user.phone}</td>
                            <td>{user.email}</td>
                            <td>{user.investmentPropensity}%</td>

                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
};

export default UserTable;
