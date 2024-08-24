import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, TextField, Box, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import { getSiparisActivity, updateSiparisActivity } from '../actions/siparis';
import { listMachines } from '../actions/machine';
import { listUsers } from '../actions/user';
import moment from 'moment-timezone';

const styles = {
    formControl: {
        width: '200px',
    },
    textField: {
        width: '200px',
    }
};

const SiparisActionPage = () => {
    const { id } = useParams();
    const [activityData, setActivityData] = useState(null);
    const [machines, setMachines] = useState([]);
    const [users, setUsers] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    // Fetch Siparis activity data
    useEffect(() => {
        getSiparisActivity(id)
            .then(resp => {
                const data = resp.data || {};
                const formattedData = {
                    ...data,
                    pressStartDateTime: formatToLocalDate(data.pressStartDateTime),
                    pressFinishDateTime: formatToLocalDate(data.pressFinishDateTime),
                    byckStartDateTime: formatToLocalDate(data.byckStartDateTime),
                    byckFinishDateTime: formatToLocalDate(data.byckFinishDateTime),
                    ovalamaStartDateTime: formatToLocalDate(data.ovalamaStartDateTime),
                    ovalamaFinishDateTime: formatToLocalDate(data.ovalamaFinishDateTime),
                    sementasyonStartDateTime: formatToLocalDate(data.sementasyonStartDateTime),
                    sementasyonFinishDateTime: formatToLocalDate(data.sementasyonFinishDateTime),
                    kaplamaStartDateTime: formatToLocalDate(data.kaplamaStartDateTime),
                    kaplamaFinishDateTime: formatToLocalDate(data.kaplamaFinishDateTime),
                    ambalajStartDateTime: formatToLocalDate(data.ambalajStartDateTime),
                    ambalajFinishDateTime: formatToLocalDate(data.ambalajFinishDateTime),
                };
                setActivityData(formattedData);
            })
            .catch(err => {
                console.error('Error fetching Siparis activity:', err);
                setError('Error fetching Siparis activity data.');
            });
    }, [id]);

    // Fetch machines and users
    useEffect(() => {
        Promise.all([listMachines(), listUsers()])
            .then(([machinesResp, usersResp]) => {
                setMachines(machinesResp.data || []);
                setUsers(usersResp.data || []);
            })
            .catch(err => {
                console.error('Error fetching machines or users:', err);
                setError('Error fetching machines or users.');
            });
    }, []);

    // Handle updating form fields
    const handleFieldChange = (field) => (event) => {
        const value = event.target ? event.target.value : '';
        setActivityData((prevData) => ({
            ...prevData,
            [field]: value || null,
        }));
    };

    // Handle submit action to update SiparisActivity
    const handleUpdate = () => {
        setLoading(true);
        const formattedActivityData = {
            ...activityData,
            pressStartDateTime: formatToUTCDate(activityData.pressStartDateTime),
            pressFinishDateTime: formatToUTCDate(activityData.pressFinishDateTime),
            byckStartDateTime: formatToUTCDate(activityData.byckStartDateTime),
            byckFinishDateTime: formatToUTCDate(activityData.byckFinishDateTime),
            ovalamaStartDateTime: formatToUTCDate(activityData.ovalamaStartDateTime),
            ovalamaFinishDateTime: formatToUTCDate(activityData.ovalamaFinishDateTime),
            sementasyonStartDateTime: formatToUTCDate(activityData.sementasyonStartDateTime),
            sementasyonFinishDateTime: formatToUTCDate(activityData.sementasyonFinishDateTime),
            kaplamaStartDateTime: formatToUTCDate(activityData.kaplamaStartDateTime),
            kaplamaFinishDateTime: formatToUTCDate(activityData.kaplamaFinishDateTime),
            ambalajStartDateTime: formatToUTCDate(activityData.ambalajStartDateTime),
            ambalajFinishDateTime: formatToUTCDate(activityData.ambalajFinishDateTime),
        };

        updateSiparisActivity(id, formattedActivityData)
            .then(() => {
                setLoading(false);
                alert('SiparisActivity updated successfully.');
            })
            .catch(err => {
                console.error('Error updating Siparis activity:', err);
                setLoading(false);
                setError('Error updating Siparis activity data.');
            });
    };

    const formatToLocalDate = (date) => {
        if (!date) return '';
        return moment(date).format('YYYY-MM-DDTHH:mm'); // Convert to 'YYYY-MM-DDTHH:MM' in local time zone
    };

    const formatToUTCDate = (date) => {
        if (!date) return null; // Preserve null values
        return moment(date).utc().format(); // Convert to ISO format with UTC timezone
    };

    if (!activityData) {
        return <Typography>Loading...</Typography>;
    }

    return (
        <Container>
            {error && <Typography color="error">{error}</Typography>}
            <Typography variant="h4" gutterBottom>
                Sipariş Aksiyonları Güncelleme
            </Typography>

            <Typography paragraph>
                {activityData.siparis.definition}
            </Typography>

            <Typography>
                <Link to={`/siparis/${activityData.siparis.id}`}>Sipariş Detaylarına Git</Link>
            </Typography>

            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Aksiyon</TableCell>
                            <TableCell>Makine</TableCell>
                            <TableCell>Operatör</TableCell>
                            <TableCell>Miktar</TableCell>
                            <TableCell>Üretim (Kg)</TableCell>
                            <TableCell>Fire (Kg)</TableCell>
                            <TableCell>Başlama Zamanı</TableCell>
                            <TableCell>Bitiş Zamanı</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {['press', 'byck', 'ovalama', 'sementasyon', 'kaplama', 'ambalaj'].map(action => (
                            <TableRow key={action}>
                                <TableCell>{action.charAt(0).toUpperCase() + action.slice(1)}</TableCell>
                                <TableCell>
                                    <FormControl sx={styles.formControl}>
                                        <InputLabel>Makine</InputLabel>
                                        <Select
                                            value={activityData[`${action}Machine`] || ''}
                                            onChange={handleFieldChange(`${action}Machine`)}
                                        >
                                            <MenuItem value="">Yok</MenuItem>
                                            {machines.map(machine => (
                                                <MenuItem key={machine.id} value={machine.id}>
                                                    {machine.name}
                                                </MenuItem>
                                            ))}
                                        </Select>
                                    </FormControl>
                                </TableCell>
                                <TableCell>
                                    <FormControl sx={styles.formControl}>
                                        <InputLabel>Operatör</InputLabel>
                                        <Select
                                            value={activityData[`${action}Operator`] || ''}
                                            onChange={handleFieldChange(`${action}Operator`)}
                                        >
                                            <MenuItem value="">Yok</MenuItem>
                                            {users && users.filter(user => user.email !== "").map(user => (
                                                <MenuItem key={user.id} value={user.id}>
                                                    {user.name}
                                                </MenuItem>
                                            ))}
                                        </Select>
                                    </FormControl>
                                </TableCell>
                                <TableCell>
                                    <TextField
                                        sx={styles.textField}
                                        value={activityData[`${action}Amount`] || ''}
                                        onChange={handleFieldChange(`${action}Amount`)}
                                    />
                                </TableCell>
                                <TableCell>
                                    <TextField
                                        sx={styles.textField}
                                        value={activityData[`${action}OutputKg`] || ''}
                                        onChange={handleFieldChange(`${action}OutputKg`)}
                                    />
                                </TableCell>
                                <TableCell>
                                    <TextField
                                        sx={styles.textField}
                                        value={activityData[`${action}WastageKg`] || ''}
                                        onChange={handleFieldChange(`${action}WastageKg`)}
                                    />
                                </TableCell>
                                <TableCell>
                                    <TextField
                                        sx={styles.textField}
                                        type="datetime-local"
                                        value={activityData[`${action}StartDateTime`] || ''}
                                        onChange={handleFieldChange(`${action}StartDateTime`)}
                                    />
                                </TableCell>
                                <TableCell>
                                    <TextField
                                        sx={styles.textField}
                                        type="datetime-local"
                                        value={activityData[`${action}FinishDateTime`] || ''}
                                        onChange={handleFieldChange(`${action}FinishDateTime`)}
                                    />
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Box sx={{ mt: 3 }}>
                <Button variant="contained" color="primary" onClick={handleUpdate} disabled={loading}>
                    {loading ? 'Güncelleniyor...' : 'Güncelle'}
                </Button>
            </Box>
        </Container>
    );
};

export default SiparisActionPage;
