import React, { useState, useEffect } from 'react';
import { fetchUsers, updateUser } from '../actions/authentication';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Switch, Typography, CircularProgress, Alert, Select, MenuItem } from '@mui/material';
import { UserType } from '../constants';

const UserListPage = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchUsers()
            .then(response => {
                let data = response.data.filter(user => user.email !== JSON.parse(localStorage.getItem('user')).email);
                data = data.sort((a, b) => { 
                    if (a.user_verified && !b.user_verified) return -1;
                    if (!a.user_verified && b.user_verified) return 1;
                    return 0;
                });
                setUsers(data);
                setLoading(false);
            })
            .catch(error => {
                setError(error);
                setLoading(false);
            });
    }, []);

    const handleToggle = (userId, field, currentValue) => {
        const updatedData = { [field]: !currentValue };
        updateUser(userId, updatedData)
            .then(() => {
                setUsers(users.map(user => 
                    user.id === userId ? { ...user, [field]: !currentValue } : user
                ));
            })
            .catch(error => {
                console.error('Error updating user:', error);
                setError(error);
            });
    };

    const handleUserTypeChange = (userId, newType) => {
        const updatedData = { user_type: newType };
        updateUser(userId, updatedData)
            .then(() => {
                setUsers(users.map(user => 
                    user.id === userId ? { ...user, user_type: newType } : user
                ));
            })
            .catch(error => {
                console.error('Error updating user type:', error);
                setError(error);
            });
    };

    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error.message}</Alert>;

    return (
        <TableContainer component={Paper}>
            <Typography variant="h4" gutterBottom component="div" align="center">
                Çalışanlar
            </Typography>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Çalışan Numarası</TableCell>
                        <TableCell>İsim/Soyisim</TableCell>
                        <TableCell>Email</TableCell>
                        <TableCell align="center">Çalışan Tipi</TableCell>
                        <TableCell align="center">Onaylandı mı</TableCell>
                        <TableCell align="center">Aktif mi</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {users.map(user => (
                        <TableRow key={user.id}>
                            <TableCell>{user.id}</TableCell>
                            <TableCell>{user.name}</TableCell>
                            <TableCell>{user.email}</TableCell>
                            <TableCell align="center">
                                <Select
                                    value={user.user_type}
                                    onChange={(e) => handleUserTypeChange(user.id, e.target.value)}
                                >
                                    {Object.values(UserType).map(type => (
                                        <MenuItem key={type} value={type}>
                                            {type}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </TableCell>
                            <TableCell align="center">
                                <Switch
                                    checked={user.user_verified}
                                    onChange={() => handleToggle(user.id, 'user_verified', user.user_verified)}
                                />
                            </TableCell>
                            <TableCell align="center">
                                <Switch
                                    checked={user.is_active}
                                    onChange={() => handleToggle(user.id, 'is_active', user.is_active)}
                                />
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default UserListPage;
