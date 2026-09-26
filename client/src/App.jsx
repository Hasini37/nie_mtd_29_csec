import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';

import Login from './Login';
import Register from './Register';
import TicketList from './TicketList';
import TicketForm from './TicketForm';

function ProtectedRoute({ children }) {
    const token = localStorage.getItem('token');

    return token ? children : <Navigate to="/login" />;
}

function Navigation() {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        navigate('/login');
    };
    return (
       <>
        <nav className="navbar navbar-dark bg-dark px-3">

            <Link className="navbar-brand" to={token ? "/tickets" : "/login"}>
                E-commerce Ticket Management
            </Link>

            <div>
                {token ? (
                    <>
                        <Link className="btn btn-light me-2" to="/tickets">
                            Tickets
                        </Link>

                        <Link className="btn btn-light me-2" to="/tickets/new">
                            New Ticket
                        </Link>

                        <Link className="btn btn-light me-2" to="/register">
                            Register
                        </Link>

                        <span className="text-white me-3">
                            {username}
                        </span>

                        <button
                            className="btn btn-danger"
                            onClick={logout}
                        >
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link className="btn btn-light me-2" to="/login">
                            Login
                        </Link>

                        <Link className="btn btn-light" to="/register">
                            Register
                        </Link>
                    </>
                )}
            </div>

        </nav>
       </>
    );
}
 
function App() {
    return (
        <>
        <BrowserRouter>

            <Navigation />

            <Routes>

                <Route
                    path="/"
                    element={
                        localStorage.getItem('token')
                            ? <Navigate to="/tickets" />
                            : <Navigate to="/login" />
                    }
                />

                <Route path="/login" element={<Login />} />

                <Route
                    path="/tickets"
                    element={
                        <ProtectedRoute>
                            <TicketList />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tickets/new"
                    element={
                        <ProtectedRoute>
                            <TicketForm />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tickets/edit/:id"
                    element={
                        <ProtectedRoute>
                            <TicketForm />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/register"
                    element={
                       
                            <Register />
                        
                    }
                />

            </Routes>

        </BrowserRouter>
       </>
    );
}

export default App;