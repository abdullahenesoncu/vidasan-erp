import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SiparisFormPage from './pages/siparis.form.page';
import SiparisListPage from './pages/siparis.list.page';
import SiparisActionPage from './pages/siparis.action.page';
import SignupPage from './pages/signup.page';
import LoginPage from './pages/login.page';
import { UserType } from './constants';
import Navbar from './Navbar'; // Import the Navbar component
import MachinePage from './pages/machine.page';

// Helper function to get the token and user type from localStorage
const getToken = () => localStorage.getItem('token');
const getUserType = () => {
    const user = JSON.parse(localStorage.getItem('user'));
    return user?.user_type;
};

// PrivateRoute component for protecting routes based on user roles and checking token
const PrivateRoute = ({ allowedRoles, element }) => {
    const token = getToken();
    const userType = getUserType();

    if (!token) {
        return <Navigate to="/login" />;
    }

    return allowedRoles.includes(userType) ? element : <Navigate to="/siparis" />;
};

// RedirectIfLoggedIn component for redirecting logged-in users away from login and signup pages
const RedirectIfLoggedIn = ({ element }) => {
    const token = getToken();
    return token ? <Navigate to="/siparis" /> : element;
};

// App component
const App = () => {
    const token = getToken();

    return (
        <Router>
            {token && <Navbar />}
            <Routes>
                <Route path="/" element={<Navigate to="/siparis" />} />
                
                <Route 
                    path="/siparis" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA, UserType.KALITE_KONTROL, UserType.DEPO]} element={<SiparisListPage />} />} 
                />

                <Route 
                    path="/siparis-press" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage process="press" />} />} 
                />

                <Route 
                    path="/siparis-byck" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage process="byck" />} />} 
                />

                <Route 
                    path="/siparis-ovalama" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage process="ovalama" />} />} 
                />

                <Route 
                    path="/siparis-sementasyon" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage process="sementasyon" />} />} 
                />

                <Route 
                    path="/siparis-kaplama" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage process="kaplama" />} />} 
                />

                <Route 
                    path="/siparis-ambalaj" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage process="ambalaj" />} />} 
                />

                <Route 
                    path="/siparis-upcoming" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage onlyUpcomingOrders={true} />} />} 
                />

                <Route 
                    path="/siparis-completed" 
                    element={<PrivateRoute allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} element={<SiparisListPage onlyCompletedOrders={true} />} />} 
                />
                
                <Route 
                    path="/siparis/create" 
                    element={
                        <PrivateRoute 
                            allowedRoles={[UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA]} 
                            element={<SiparisFormPage readonly={false} />} 
                        />
                    } 
                />
                
                <Route 
                    path="/siparis/:id" 
                    element={
                        <PrivateRoute 
                            allowedRoles={[UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA, UserType.KALITE_KONTROL, UserType.DEPO]}
                            element={<SiparisFormPage readonly={![UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA].includes(getUserType())} />}
                        />
                    } 
                />

                <Route 
                    path="/siparis-activity/:id" 
                    element={
                        <PrivateRoute 
                            allowedRoles={[UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA, UserType.KALITE_KONTROL, UserType.DEPO]}
                            element={<SiparisActionPage readonly={![UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA].includes(getUserType())} />}
                        />
                    } 
                />

                <Route 
                    path="/machine" 
                    element={
                        <PrivateRoute 
                            allowedRoles={[UserType.ADMIN, UserType.PLANLAMA]} 
                            element={<MachinePage />}
                        />
                    } 
                />

                <Route 
                    path="/signup" 
                    element={<RedirectIfLoggedIn element={<SignupPage />} />} 
                />
                <Route 
                    path="/login" 
                    element={<RedirectIfLoggedIn element={<LoginPage />} />} 
                />
            </Routes>
        </Router>
    );
};

export default App;
