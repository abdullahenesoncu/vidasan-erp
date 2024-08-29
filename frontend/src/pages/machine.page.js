import React, { useState, useEffect } from 'react';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, TextField, Box, MenuItem, Select, InputLabel, FormControl, Snackbar, Alert, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { listMachines, createMachine, getMachine, updateMachine, deleteMachine } from '../actions/machine';
import { useNavigate, useParams } from 'react-router-dom';
import { MachineType, MachineVariation } from '../constants'; // Import constants

const styles = {
    formControl: {
        width: '200px',
    },
    textField: {
        width: '200px',
    }
};

const MachinePage = () => {
    const [machines, setMachines] = useState([]);
    const [filteredMachines, setFilteredMachines] = useState([]);
    const [selectedMachine, setSelectedMachine] = useState(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [dialogType, setDialogType] = useState('create');
    const [formData, setFormData] = useState({ name: '', type: '', variation: '' });
    const [filterType, setFilterType] = useState(''); // For filtering by type
    const [filterVariation, setFilterVariation] = useState(''); // For filtering by variation
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [loading, setLoading] = useState(false);
    const [sortField, setSortField] = useState('name'); // Default sort field
    const [sortDirection, setSortDirection] = useState('asc'); // Default sort direction
    const navigate = useNavigate();
    const { id } = useParams();

    useEffect(() => {
        fetchMachines();
        if (id) {
            fetchMachine(id);
        }
    }, [id, sortField, sortDirection]);

    useEffect(() => {
        filterMachines();
    }, [machines, filterType, filterVariation]);

    const fetchMachines = async () => {
        try {
            const response = await listMachines();
            let sortedMachines = response.data;
            
            // Sort machines based on sortField and sortDirection
            sortedMachines = sortedMachines.sort((a, b) => {
                if (a[sortField] < b[sortField]) return sortDirection === 'asc' ? -1 : 1;
                if (a[sortField] > b[sortField]) return sortDirection === 'asc' ? 1 : -1;
                return 0;
            });

            setMachines(sortedMachines);
        } catch (err) {
            setError('Failed to fetch machines.');
        }
    };

    const fetchMachine = async (id) => {
        try {
            const response = await getMachine(id);
            setFormData(response.data);
        } catch (err) {
            setError('Failed to fetch machine details.');
        }
    };

    const filterMachines = () => {
        const filtered = machines.filter(machine => {
            return (
                (filterType ? machine.type === filterType : true) &&
                (filterVariation ? machine.variation === filterVariation : true)
            );
        });
        setFilteredMachines(filtered);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        if (name === 'filterType') setFilterType(value);
        if (name === 'filterVariation') setFilterVariation(value);
    };

    const handleOpenDialog = (type, machine = null) => {
        setDialogType(type);
        if (machine) {
            setSelectedMachine(machine);
            setFormData(machine);
        } else {
            setFormData({ name: '', type: '', variation: '' });
        }
        setIsDialogOpen(true);
    };

    const handleCloseDialog = () => {
        setIsDialogOpen(false);
        setSelectedMachine(null);
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            if (dialogType === 'create') {
                await createMachine(formData);
                setSuccess('Machine created successfully.');
            } else if (dialogType === 'edit') {
                await updateMachine(selectedMachine.id, formData);
                setSuccess('Machine updated successfully.');
            }
            fetchMachines();
        } catch (err) {
            setError(`Failed to ${dialogType === 'create' ? 'create' : 'update'} machine.`);
        } finally {
            setLoading(false);
            handleCloseDialog();
        }
    };

    const handleDelete = async (id) => {
        const isConfirmed = window.confirm('Are you sure you want to delete this machine?');
        if (!isConfirmed) {
            return;
        }
        
        setLoading(true);
        try {
            await deleteMachine(id);
            setSuccess('Machine deleted successfully.');
            fetchMachines();
        } catch (err) {
            setError('Failed to delete machine.');
        } finally {
            setLoading(false);
        }
    };

    const handleSortChange = (field) => {
        const newDirection = sortField === field && sortDirection === 'asc' ? 'desc' : 'asc';
        setSortField(field);
        setSortDirection(newDirection);
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Makine Yönetimi
            </Typography>

            {error && <Alert severity="error">{error}</Alert>}
            {success && <Alert severity="success">{success}</Alert>}

            <Box sx={{ mb: 3 }}>
                <FormControl sx={styles.formControl}>
                    <InputLabel>Filter by Type</InputLabel>
                    <Select
                        name="filterType"
                        value={filterType}
                        onChange={handleFilterChange}
                    >
                        <MenuItem value="">All</MenuItem>
                        {Object.entries(MachineType).map(([key, value]) => (
                            <MenuItem key={value} value={value}>{key}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl sx={styles.formControl} style={{ marginLeft: '20px' }}>
                    <InputLabel>Filter by Variation</InputLabel>
                    <Select
                        name="filterVariation"
                        value={filterVariation}
                        onChange={handleFilterChange}
                    >
                        <MenuItem value="">All</MenuItem>
                        {Object.entries(MachineVariation).map(([key, value]) => (
                            <MenuItem key={value} value={value}>{key}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>

            <Box sx={{ mb: 3 }}>
                <Button variant="contained" color="primary" onClick={() => handleOpenDialog('create')}>
                    Add New Machine
                </Button>
            </Box>

            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell onClick={() => handleSortChange('name')} style={{ cursor: 'pointer' }}>
                                Name {sortField === 'name' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
                            </TableCell>
                            <TableCell onClick={() => handleSortChange('type')} style={{ cursor: 'pointer' }}>
                                Type {sortField === 'type' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
                            </TableCell>
                            <TableCell onClick={() => handleSortChange('variation')} style={{ cursor: 'pointer' }}>
                                Variation {sortField === 'variation' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
                            </TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filteredMachines.map(machine => (
                            <TableRow key={machine.id}>
                                <TableCell>{machine.name}</TableCell>
                                <TableCell>{machine.type}</TableCell>
                                <TableCell>{machine.variation}</TableCell>
                                <TableCell>
                                    <Button variant="outlined" color="primary" onClick={() => handleOpenDialog('edit', machine)}>
                                        Düzenle
                                    </Button>
                                    <Button variant="outlined" color="error" onClick={() => handleDelete(machine.id)}>
                                        Sil
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={isDialogOpen} onClose={handleCloseDialog}>
                <DialogTitle>{dialogType === 'create' ? 'Add New Machine' : 'Edit Machine'}</DialogTitle>
                <DialogContent>
                    <TextField
                        margin="dense"
                        label="Name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        fullWidth
                        variant="outlined"
                    />
                    <FormControl sx={styles.formControl} margin="dense">
                        <InputLabel>Type</InputLabel>
                        <Select
                            name="type"
                            value={formData.type}
                            onChange={handleChange}
                        >
                            {Object.entries(MachineType).map(([key, value]) => (
                                <MenuItem key={value} value={value}>{key}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl sx={styles.formControl} margin="dense">
                        <InputLabel>Variation</InputLabel>
                        <Select
                            name="variation"
                            value={formData.variation}
                            onChange={handleChange}
                        >
                            {Object.entries(MachineVariation).map(([key, value]) => (
                                <MenuItem key={value} value={value}>{key}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleSave} color="primary" disabled={loading}>
                        {loading ? 'Saving...' : 'Save'}
                    </Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
};

export default MachinePage;
