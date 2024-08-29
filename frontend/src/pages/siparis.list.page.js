import React, { useState, useEffect } from 'react';
import {
    Container, Typography, TextField, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, 
    Checkbox, IconButton, Paper, Box, Pagination, Stack, Button,
    FormControl,
    InputLabel,
    Select,
    MenuItem
} from '@mui/material';
import { listSiparis, deleteSiparis, downloadWorkOrderExcel, updateSiparis } from '../actions/siparis';
import { ArrowUpward, ArrowDownward, Add, Edit, Download } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { ProcessState, ProcessTransitions, SiparisState } from '../constants';

const SiparisListPage = ({process, onlyUpcomingOrders=false, onlyCompletedOrders=false}) => {
    const [siparisList, setSiparisList] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedSiparisler, setSelectedSiparisler] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage] = useState(10);
    const [pageCount, setPageCount] = useState(0);
    const [sortField, setSortField] = useState('orderDate');
    const [sortOrder, setSortOrder] = useState('desc');
    const [colors, setColors] = useState( [] );
    const navigate = useNavigate();

    useEffect(() => {
        fetchSiparisList();
    }, [currentPage, searchTerm, sortField, sortOrder, process, onlyUpcomingOrders, onlyCompletedOrders]);

    useEffect(() => {
        setCurrentPage(1); // Reset to page 1 when search term changes
    }, [searchTerm]);

    useEffect(() => {
        if ( process ) {
            const processStateName = process + 'State';
            setColors(
                siparisList.map( siparis => {
                    if ( siparis[ processStateName ] == ProcessState.BASLAMADI ) return '#d1cfc8';
                    else if ( siparis[ processStateName ] == ProcessState.CALISIYOR ) return '#6FC276';
                    else if ( siparis[ processStateName ] == ProcessState.BEKLEMEDE ) return '#f4f186';
                    else if ( siparis[ processStateName ] == ProcessState.BITTI ) return '#f47174';
                } ) );
        }
        else {
            setColors(
                siparisList.map( siparis => {
                    if ( siparis.state == SiparisState.PLANLAMA ) return '#d1cfc8';
                    else if ( siparis.state == SiparisState.IMALAT ) return '#f4f186';
                    else if ( siparis.state == SiparisState.SIPARIS_TAMAMLANDI ) return '#f47174';
                } ) );
        }
    }, [siparisList, process]);

    const fetchSiparisList = () => {
        listSiparis( currentPage, searchTerm, sortField, sortOrder, onlyUpcomingOrders, onlyCompletedOrders )
            .then( resp => {
                setPageCount(Math.ceil(resp.data.count / itemsPerPage));
                setSiparisList(resp.data.results);
            } )
            .catch( (error) => {
                console.error('Error fetching siparis data:', error);
            } );
    }

    const handlePageChange = (event, value) => {
        setCurrentPage(value);
    };

    const handleSelect = (id) => {
        setSelectedSiparisler((prevSelected) => 
            prevSelected.includes(id) 
                ? prevSelected.filter(itemId => itemId !== id) 
                : [...prevSelected, id]
        );
    };

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

    const handleSort = (field) => {
        const isAsc = sortField === field && sortOrder === 'asc';
        setSortField(field);
        setSortOrder(isAsc ? 'desc' : 'asc');
    };

    const handleCreateSiparis = () => {
        navigate('/siparis/create');
    };

    const handleUpdateSiparis = (id) => {
        navigate(`/siparis/${id}`);
    };

    const handleDownload = (id) => {
        downloadWorkOrderExcel(id);
    };

    const handleProcessStateChange = ( siparis, newState ) => {
        siparis[ process + 'State' ] = newState;
        updateSiparis( siparis.id, siparis )
            .then( () => fetchSiparisList() )
            .catch( () => console.log( "An error occured when updating siparis process state" ) );
    }

    function capitalizeFirstChar(str) {
        if (!str) return str;  // Return if the string is empty or undefined
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

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
                            <TableCell>Seç</TableCell>
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
                                    Sipariş Tarihi
                                    <IconButton onClick={() => handleSort('orderDate')}>
                                        {sortField === 'orderDate' && sortOrder === 'asc' ? 
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
                            {process && (
                                <TableCell>{capitalizeFirstChar(process)} Durumu</TableCell> 
                            )}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {siparisList.map((siparis, index) => (
                            <TableRow key={siparis.id} sx={{ backgroundColor: colors[index] }}>
                                <TableCell>
                                    <Checkbox
                                        checked={selectedSiparisler.includes(siparis.id)}
                                        onChange={() => handleSelect(siparis.id)}
                                    />
                                </TableCell>
                                <TableCell>{siparis.definition}</TableCell>
                                <TableCell>{siparis.description.length > 50 ? `${siparis.description.substring(0, 50)}...` : siparis.description}</TableCell>
                                <TableCell>{new Date(siparis.deadline).toLocaleDateString()}</TableCell>
                                <TableCell>{new Date(siparis.orderDate).toLocaleDateString()}</TableCell>
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
                                <TableCell>
                                    {process && (
                                        <FormControl fullWidth margin="normal">
                                            <InputLabel>Durum Değiştir</InputLabel>
                                            <Select
                                                name="processState"
                                                value={siparis[ process + 'State' ]}
                                                label="processState"
                                                onChange={(e) => handleProcessStateChange( siparis, e.target.value )}
                                            >
                                                {ProcessTransitions[ siparis[ process + 'State' ] ]?.map(key => (
                                                    <MenuItem key={key} value={key}>
                                                        {key}
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                        </FormControl>
                                    )}
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
