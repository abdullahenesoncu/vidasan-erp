import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { TextField, Button, Container, Typography, Box, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import { createSiparis, getNextStep, getSiparis, goNextStep, updateSiparis, listSiparisFiles, createSiparisFile, deleteSiparisFile } from '../actions/siparis';
import { listKaplama, listIsilIslem, listPatch } from '../actions/vidasan';

const SiparisFormPage = ({ readonly = false }) => {
    const [formData, setFormData] = useState({
        definition: '',
        description: '',
        amount: '',
        isOEM: false,
        isActive: false,
        orderNumber: '',
        kaplama_id: '',
        isilIslem_id: '',
        patch_id: '',
        deadline: '',
        state: '',
    });
    const [fileData, setFileData] = useState(null);
    const [siparisFiles, setSiparisFiles] = useState([]);
    const { id } = useParams();
    const navigate = useNavigate();
    const [isUpdate, setIsUpdate] = useState(false);
    const [kaplamaOptions, setKaplamaOptions] = useState([]);
    const [isilIslemOptions, setIsilIslemOptions] = useState([]);
    const [patchOptions, setPatchOptions] = useState([]);
    const [nextStep, setNextStep] = useState(null);

    useEffect(() => {
        Promise.all([listKaplama(), listIsilIslem(), listPatch()])
            .then(([kaplamaRes, isilIslemRes, patchRes]) => {
                setKaplamaOptions(kaplamaRes.data);
                setIsilIslemOptions(isilIslemRes.data);
                setPatchOptions(patchRes.data);
            })
            .catch((error) => {
                console.error('Error fetching options data:', error);
            });

        if (id) {
            listSiparisFiles(id)
                .then(resp => setSiparisFiles(resp.data));
            getNextStep(id)
                .then(resp => setNextStep(resp.data.nextStep));
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            setIsUpdate(true);
            getSiparis(id)
                .then((response) => {
                    setFormData({
                        definition: response.data.definition,
                        description: response.data.description,
                        amount: response.data.amount,
                        isOEM: response.data.isOEM,
                        isActive: response.data.isActive,
                        orderNumber: response.data.orderNumber,
                        kaplama_id: response.data.kaplama?.id || '',
                        isilIslem_id: response.data.isilIslem?.id || '',
                        patch_id: response.data.patch?.id || '',
                        deadline: response.data.deadline ? new Date(response.data.deadline).toISOString().split('T')[0] : '',
                        state: response.data.state || '',
                    });
                })
                .catch((error) => {
                    navigate('/siparis');
                });
        }
    }, [id]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData((prevState) => ({
            ...prevState,
            [name]: type === 'checkbox' ? checked : value,
        }));
    };

    const handleFileChange = (e) => {
        setFileData(e.target.files[0]);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const payload = { ...formData };

        if (isUpdate) {
            updateSiparis(id, payload)
                .then((response) => {
                    console.log('Siparis updated:', response.data);
                    navigate('/siparis');
                })
                .catch((error) => {
                    console.error('Error updating Siparis:', error);
                });
        } else {
            createSiparis(payload)
                .then((response) => {
                    navigate(`/siparis/${response.data.id}`);
                })
                .catch((error) => {
                    console.error('Error creating Siparis:', error);
                });
        }
    };

    const handleNextStep = () => {
        if (nextStep) {
            if (!window.confirm(`Gerçekten '${nextStep}' istiyor musunuz?`)) return;
            goNextStep(id)
                .then(_ => {
                    window.location.reload();
                });
        }
    };

    const handleFileUpload = () => {
        if (!fileData) return;

        const formData = new FormData();
        formData.append('file', fileData);
        formData.append('title', fileData.name); // Set the file title to be its name

        createSiparisFile(id, formData)
            .then(response => {
                console.log('File uploaded:', response.data);
                setSiparisFiles([...siparisFiles, response.data]);
                setFileData(null); // Clear file input
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
    };

    const handleFileDelete = (fileId) => {
        if (!window.confirm('Are you sure you want to delete this file?')) return;

        deleteSiparisFile(id, fileId)
            .then(() => {
                console.log('File deleted:', fileId);
                setSiparisFiles(siparisFiles.filter(file => file.id !== fileId));
            })
            .catch(error => {
                console.error('Error deleting file:', error);
            });
    };

    console.log( siparisFiles?.map(file=>file) );

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                {isUpdate ? (readonly ? 'Sipariş Görüntüleme' : 'Sipariş Düzenleme') : 'Sipariş Oluşturma'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 3 }}>
                <TextField
                    fullWidth
                    label="İş Tanımı"
                    name="definition"
                    value={formData.definition}
                    onChange={handleChange}
                    margin="normal"
                    required
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <TextField
                    fullWidth
                    label="Açıklama"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    margin="normal"
                    required
                    multiline
                    rows={4}
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <TextField
                    fullWidth
                    label="Adet"
                    name="amount"
                    value={formData.amount}
                    onChange={handleChange}
                    margin="normal"
                    type="number"
                    required
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <TextField
                    fullWidth
                    label="Sipariş Numarası"
                    name="orderNumber"
                    value={formData.orderNumber}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <TextField
                    fullWidth
                    label="Termin Tarihi"
                    name="deadline"
                    value={formData.deadline}
                    onChange={handleChange}
                    margin="normal"
                    type="date"
                    InputLabelProps={{ shrink: true }}
                    InputProps={{
                        readOnly: readonly,
                    }}
                />

                <FormControl fullWidth margin="normal">
                    <InputLabel id="kaplama-label">Kaplama</InputLabel>
                    <Select
                        labelId="kaplama-label"
                        name="kaplama_id"
                        value={formData.kaplama_id}
                        onChange={handleChange}
                        inputProps={{
                            readOnly: readonly,
                        }}
                    >
                        <MenuItem value={null}>Yok</MenuItem>
                        {kaplamaOptions.map((option) => (
                            <MenuItem key={option.id} value={option.id}>
                                {option.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <FormControl fullWidth margin="normal">
                    <InputLabel id="isilIslem-label">Isil Islem</InputLabel>
                    <Select
                        labelId="isilIslem-label"
                        name="isilIslem_id"
                        value={formData.isilIslem_id}
                        onChange={handleChange}
                        inputProps={{
                            readOnly: readonly,
                        }}
                    >
                        <MenuItem value={null}>Yok</MenuItem>
                        {isilIslemOptions.map((option) => (
                            <MenuItem key={option.id} value={option.id}>
                                {option.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <FormControl fullWidth margin="normal">
                    <InputLabel id="patch-label">Patch</InputLabel>
                    <Select
                        labelId="patch-label"
                        name="patch_id"
                        value={formData.patch_id}
                        onChange={handleChange}
                        inputProps={{
                            readOnly: readonly,
                        }}
                    >
                        <MenuItem value={null}>Yok</MenuItem>
                        {patchOptions.map((option) => (
                            <MenuItem key={option.id} value={option.id}>
                                {option.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {/* File Upload Section */}
                {id && (
                    <Box sx={{ mt: 3 }}>
                        <input
                            type="file"
                            onChange={handleFileChange}
                            disabled={readonly}
                        />
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleFileUpload}
                            sx={{ mt: 2 }}
                            disabled={readonly || !fileData}
                        >
                            Upload File
                        </Button>

                        <Typography variant="h6" sx={{ mt: 3 }}>
                            Uploaded Files:
                        </Typography>
                        <ul>
                            {siparisFiles.map(file => (
                                <li key={file.id}>
                                    <a href={file.file} download>
                                        {file.title}
                                    </a>
                                    <Button
                                        variant="outlined"
                                        color="error"
                                        onClick={() => handleFileDelete(file.id)}
                                        sx={{ ml: 2 }}
                                    >
                                        Delete
                                    </Button>
                                </li>
                            ))}
                        </ul>
                    </Box>
                )}

                {id && (
                    <TextField
                        fullWidth
                        label="Durum"
                        name="state"
                        value={formData.state}
                        margin="normal"
                        InputProps={{
                            readOnly: true,
                        }}
                    />
                )}

                {(
                    <>
                        <Button type="submit" variant="contained" color="primary" sx={{ mt: 3 }}>
                            {isUpdate ? 'Değişiklikleri Kaydet' : 'Sipariş Oluştur'}
                        </Button>
                        {nextStep && (
                            <Button
                                variant="contained"
                                color="secondary"
                                onClick={() => handleNextStep()}
                                sx={{ mt: 2, ml: 2 }}
                            >
                                {nextStep}
                            </Button>
                        )}
                    </>
                )}
            </Box>
        </Container>
    );
};

export default SiparisFormPage;
