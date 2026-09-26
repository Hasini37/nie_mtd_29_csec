import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from './api';

function TicketForm() {

    const navigate = useNavigate();
    const { id } = useParams();

    const [form, setForm] = useState({
        title: '',
        description: '',
        category: '',
        status: 'NEW'
    });

    const token = localStorage.getItem('token');

    useEffect(() => {
        if (id) {
            getTicket();
        }
    }, [id]);

    const getTicket = async () => {
        const response = await api.get(`/tickets/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        setForm(response.data);
    };

    const saveTicket = async () => {

        if (id) {
            await api.put(`/tickets/${id}`, form, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            alert('Ticket updated');
        } else {
            await api.post('/tickets', form, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            alert('Ticket created');
        }

        navigate('/tickets');
    };

    return (
        <div className="container mt-4">

            <div className="card p-4 mx-auto" style={{maxWidth: '600px'}}>

                <h2>
                    {id ? 'Edit Ticket' : 'New Ticket'}
                </h2>

                <label className="form-label">Title</label>

                <input
                    className="form-control mb-3"
                    value={form.title}
                    onChange={e =>
                        setForm({
                            ...form,
                            title: e.target.value
                        })
                    }
                />

                <label className="form-label">Description</label>

                <textarea
                    className="form-control mb-3"
                    value={form.description}
                    onChange={e =>
                        setForm({
                            ...form,
                            description: e.target.value
                        })
                    }
                />

                <label className="form-label">Category</label>

                <select
                    className="form-select mb-3"
                    value={form.category}
                    onChange={e =>
                        setForm({
                            ...form,
                            category: e.target.value
                        })
                    }
                >
                    <option value="">Select Category</option>
                    <option value="Product">Product</option>
                    <option value="Payment">Payment</option>
                    <option value="Delivery">Delivery</option>
                    <option value="Refund">Refund</option>
                    <option value="Other">Other</option>
                </select>

                <label className="form-label">Status</label>

                <select
                    className="form-select mb-3"
                    value={form.status}
                    onChange={e =>
                        setForm({
                            ...form,
                            status: e.target.value
                        })
                    }
                >
                    <option value="NEW">NEW</option>
                    <option value="ASSIGNED">ASSIGNED</option>
                    <option value="IN_PROGRESS">IN_PROGRESS</option>
                    <option value="ON_HOLD">ON_HOLD</option>
                    <option value="RESOLVED">RESOLVED</option>
                    <option value="CLOSED">CLOSED</option>
                </select>

                <button
                    className="btn btn-primary"
                    onClick={saveTicket}
                >
                    {id ? 'Update Ticket' : 'Create Ticket'}
                </button>

            </div>

        </div>
    );
}

export default TicketForm;