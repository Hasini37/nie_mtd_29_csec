import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';

function Login() {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        username: '',
        password: ''
    });

    const login = async () => {
        const data = new URLSearchParams();

        data.append('username', form.username);
        data.append('password', form.password);

        const response = await api.post('/login', data);

        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('username', form.username);
        
        navigate('/tickets');
    };
    


    return (
        <div className="container mt-5">
            <div
                className="card p-4 mx-auto"
                style={{maxWidth: '400px'}}
            >
                <h2 className="text-center mb-4">
                    Ticket Management
                </h2>

                <label className="form-label">
                    Username
                </label>

                <input
                    className="form-control mb-3"
                    value={form.username}
                    onChange={e =>
                        setForm({
                            ...form,
                            username: e.target.value
                        })
                    }
                />

                <label className="form-label">
                    Password
                </label>

                <input
                    type="password"
                    className="form-control mb-3"
                    value={form.password}
                    onChange={e =>
                        setForm({
                            ...form,
                            password: e.target.value
                        })
                    }
                />

                <button
                    className="btn btn-primary"
                    onClick={login}
                >
                    Login
                </button>
            </div>
        </div>
        
    );
}

export default Login;