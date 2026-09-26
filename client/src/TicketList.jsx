import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';

function TicketList() {
    const navigate = useNavigate();

    const [tickets, setTickets] = useState([]);

    const getTickets = async () => {
        const response = await api.get('/tickets', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        });

        setTickets(response.data);
    };

    const deleteTicket = async (id) => {
        await api.delete(`/tickets/${id}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        });

        getTickets();
    };

    useEffect(() => {
        getTickets();
    }, []);

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between mb-3">
                <h2>Tickets</h2>
                <button
                    className="btn btn-primary"
                    onClick={() => navigate('/tickets/new')}
                >New Ticket</button>
            </div>
            <table className="table table-bordered table-striped">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {tickets.map(ticket => (
                        <tr key={ticket.id}>
                            <td>{ticket.title}</td>
                            <td>{ticket.description}</td>
                            <td>{ticket.category}</td>
                            <td>{ticket.status}</td>
                            <td>
                                <button
                                    className="btn btn-warning btn-sm me-2"
                                    onClick={() =>
                                        navigate(`/tickets/edit/${ticket.id}`)
                                    }
                                >Edit</button>
                                <button
                                    className="btn btn-danger btn-sm"
                                    onClick={() =>
                                        deleteTicket(ticket.id)
                                    }
                                >Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default TicketList;