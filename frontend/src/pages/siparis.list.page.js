import React, { useState, useEffect } from 'react';
import {
    Container, Typography, TextField, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, 
    Checkbox, IconButton, Paper, Box, Pagination, Stack, Button
} from '@mui/material';
import { listSiparis, deleteSiparis, downloadWorkOrderPDF } from '../actions/siparis';
import { ArrowUpward, ArrowDownward, Add, Edit, Download } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const SiparisListPage = () => {
    const [siparisList, setSiparisList] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedSiparisler, setSelectedSiparisler] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage] = useState(10);
    const [pageCount, setPageCount] = useState(0);
    const [sortField, setSortField] = useState('definition'); // Default sort field
    const [sortOrder, setSortOrder] = useState('asc'); // Default sort order
    const navigate = useNavigate(); // Initialize navigate

    // Fetch data on initial load and when pagination, filters, or sort order change
    useEffect(() => {
        fetchSiparisList();
    }, [currentPage, searchTerm, sortField, sortOrder]);

    const fetchSiparisList = async () => {
        try {
            const response = await listSiparis(); // Fetch Siparis data from API
            const filteredData = filterSiparis(response.data);
            const sortedData = sortSiparis(filteredData);
            setPageCount(Math.ceil(sortedData.length / itemsPerPage));
            setSiparisList(sortedData.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage));
        } catch (error) {
            console.error('Error fetching siparis data:', error);
        }
    };

    // Filter data by search term
    const filterSiparis = (siparisData) => {
        return siparisData.filter((siparis) => {
            const matchesSearch = siparis.definition.toLowerCase().includes(searchTerm.toLowerCase()) ||
                                  siparis.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                                  siparis.kaplama?.name?.toLowerCase().includes(searchTerm.toLowerCase());

            return matchesSearch;
        });
    };

    // Sort data by selected field and order
    const sortSiparis = (siparisData) => {
        return siparisData.sort((a, b) => {
            if (sortOrder === 'asc') {
                return a[sortField] > b[sortField] ? 1 : -1;
            } else {
                return a[sortField] < b[sortField] ? 1 : -1;
            }
        });
    };

    // Handle pagination change
    const handlePageChange = (event, value) => {
        setCurrentPage(value);
    };

    // Handle selecting/deselecting a Siparis item
    const handleSelect = (id) => {
        setSelectedSiparisler((prevSelected) => 
            prevSelected.includes(id) 
                ? prevSelected.filter(itemId => itemId !== id) 
                : [...prevSelected, id]
        );
    };

    // Handle bulk deletion of selected Siparis items
    const handleDeleteSelected = async () => {
        if (!window.confirm(`Do you really want to delete ${selectedSiparisler.length} siparis?`)) return;
        try {
            for (const id of selectedSiparisler) {
                await deleteSiparis(id);
            }
            setSelectedSiparisler([]);
            fetchSiparisList();  // Refresh the list after deletion
        } catch (error) {
            console.error('Error deleting siparis:', error);
        }
    };

    // Handle sorting
    const handleSort = (field) => {
        const isAsc = sortField === field && sortOrder === 'asc';
        setSortField(field);
        setSortOrder(isAsc ? 'desc' : 'asc');
    };

    // Handle row click to navigate to details page
    const handleRowClick = (id) => {
        navigate(`/siparis/${id}`);
    };

    // Handle navigate to create siparis page
    const handleCreateSiparis = () => {
        navigate('/siparis/create');
    };

    // Handle navigate to update siparis page
    const handleUpdateSiparis = (id) => {
        navigate(`/siparis/${id}`);
    };

    // Handle download work order PDF
    const handleDownload = (id) => {
        downloadWorkOrderPDF(id);
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>Siparişler</Typography>

            {/* Search and Create Controls */}
            <Box display="flex" justifyContent="space-between" alignItems="center" marginBottom={2}>
                <TextField
                    label="Sipariş Ara"
                    variant="outlined"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{ flex: 1 }}
                />
                <IconButton color="primary" onClick={handleCreateSiparis} sx={{ ml: 2 }}>
                    <Add />
                </IconButton>
            </Box>

            {/* Delete Selected Button */}
            <Button
                variant="contained"
                color="secondary"
                onClick={handleDeleteSelected}
                disabled={selectedSiparisler.length === 0}
            >
                Seçilenleri Sil
            </Button>

            {/* Siparis Table */}
            <TableContainer component={Paper} style={{ marginTop: 20 }}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Select</TableCell>
                            <TableCell>
                                <Box display="flex" alignItems="center">
                                    Tanım
                                    <IconButton onClick={() => handleSort('definition')}>
                                        {sortField === 'definition' && sortOrder === 'asc' ? 
                                            <ArrowUpward /> : <ArrowDownward />}
                                    </IconButton>
                                </Box>
                            </TableCell>
                            <TableCell>
                                <Box display="flex" alignItems="center">
                                    Açıklama
                                    <IconButton onClick={() => handleSort('description')}>
                                        {sortField === 'description' && sortOrder === 'asc' ? 
                                            <ArrowUpward /> : <ArrowDownward />}
                                    </IconButton>
                                </Box>
                            </TableCell>
                            <TableCell>
                                <Box display="flex" alignItems="center">
                                    Termin Tarihi
                                    <IconButton onClick={() => handleSort('deadline')}>
                                        {sortField === 'deadline' && sortOrder === 'asc' ? 
                                            <ArrowUpward /> : <ArrowDownward />}
                                    </IconButton>
                                </Box>
                            </TableCell>
                            <TableCell>
                                <Box display="flex" alignItems="center">
                                    Oluşturulma Zamanı
                                    <IconButton onClick={() => handleSort('created_at')}>
                                        {sortField === 'created_at' && sortOrder === 'asc' ? 
                                            <ArrowUpward /> : <ArrowDownward />}
                                    </IconButton>
                                </Box>
                            </TableCell>
                            <TableCell>
                                <Box display="flex" alignItems="center">
                                    Durum
                                    <IconButton onClick={() => handleSort('state')}>
                                        {sortField === 'state' && sortOrder === 'asc' ? 
                                            <ArrowUpward /> : <ArrowDownward />}
                                    </IconButton>
                                </Box>
                            </TableCell>
                            <TableCell>Aksiyonlar</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {siparisList.map((siparis) => (
                            <TableRow key={siparis.id} hover onClick={() => handleRowClick(siparis.id)}>
                                <TableCell>
                                    <Checkbox
                                        checked={selectedSiparisler.includes(siparis.id)}
                                        onChange={() => handleSelect(siparis.id)}
                                    />
                                </TableCell>
                                <TableCell>{siparis.definition}</TableCell>
                                <TableCell>{siparis.description.length > 50 ? `${siparis.description.substring(0, 50)}...` : siparis.description}</TableCell>
                                <TableCell>{new Date(siparis.deadline).toLocaleDateString()}</TableCell>
                                <TableCell>{new Date(siparis.created_at).toLocaleDateString()}</TableCell>
                                <TableCell>{siparis.state}</TableCell>
                                <TableCell>
                                    <IconButton color="primary" onClick={(e) => {
                                        e.stopPropagation(); // Prevent row click event
                                        handleUpdateSiparis(siparis.id);
                                    }}>
                                        <Edit />
                                    </IconButton>
                                    <IconButton color="primary" onClick={(e) => {
                                        e.stopPropagation(); // Prevent row click event
                                        handleDownload(siparis.id);
                                    }}>
                                        <Download />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Pagination */}
            <Stack spacing={2} marginTop={2}>
                <Pagination
                    count={pageCount}
                    page={currentPage}
                    onChange={handlePageChange}
                    color="primary"
                />
            </Stack>
        </Container>
    );
};

export default SiparisListPage;
