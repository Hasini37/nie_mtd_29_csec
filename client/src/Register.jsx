import { useState } from 'react';
import api from './api';

function Register() {
    const [form, setForm] = useState({username:'', password:'', role:1});
    const register = async () => {
        try {            
            const response = await api.post('/users', {... form});
            if(response.status !== 201) {
                alert(response.data.detail);
                return;
            }
            alert('User created');
            setForm({username:'', password:'', role:1});
        } catch(error) {
            alert(error.response?.data?.detail || 'User creation failed');
        }
    };
    return (
       <div className="container mt-4">
            <div className="card p-4 mx-auto" style={{maxWidth: '500px'}}>
                <h2>Create User</h2>
                <label className="form-label">
                    Username
                </label>
                <input
                    className="form-control mb-3"
                    value={form.username}
                    onChange={ e => setForm( {...form, username:e.target.value} ) }
                />
                <label className="form-label">Password</label>

                <input
                    type="password"
                    className="form-control mb-3"
                    value={form.password}
                    onChange={ e => setForm( {...form, password:e.target.value} ) }
                />

                <label className="form-label">Role</label>

                <select
                    className="form-select mb-3"
                    value={form.role}
                    onChange={ e => setForm( {...form, role:Number(e.target.value)} ) } >
                    <option value="1">Employee</option>
                    <option value="2">Engineer</option>
                    <option value="3">Lead</option>
                    <option value="4">Admin</option>
                </select>

                <button className="btn btn-primary" onClick={register}>Create User</button>
            </div>
        </div>
    );
}

export default Register;