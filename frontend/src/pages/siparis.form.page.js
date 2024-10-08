import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { TextField, Button, Container, Typography, Box, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import { Link } from 'react-router-dom';
import { createSiparis, getSiparis, updateSiparis, listSiparisFiles, createSiparisFile, deleteSiparisFile, goNextStep, getNextStep } from '../actions/siparis';
import { KaplamaTypes, QualityTypes, Materials, ProcessTransitions } from '../constants';

const SiparisFormPage = ({ readonly = false }) => {
    const [formData, setFormData] = useState({
        activityId: null,
        definition: '',
        description: '',
        amount: '',
        isOEM: false,
        isActive: false,
        orderNumber: '',
        clientOrderNumber: '',
        materialNumber: '',
        company: '',
        kaplama: '',
        quality: '',
        patch: '',
        material: '',
        deadline: '',
        orderDate: '',
        state: '',
        pressState: '',
        byckState: '',
        ovalamaState: '',
        sementasyonState: '',
        kaplamaState: '',
        ambalajState: '',
    });
    const [fileData, setFileData] = useState(null);
    const [siparisFiles, setSiparisFiles] = useState([]);
    const { id } = useParams();
    const navigate = useNavigate();
    const [isUpdate, setIsUpdate] = useState(false);
    const [nextStep, setNextStep] = useState(null);
    const [error, setError] = useState(null);
    const [pressState, setPressState] = useState( null );
    const [byckState, setByckState] = useState( null );
    const [ovalamaState, setOvalamaState] = useState( null );
    const [sementasyonState, setSementasyonState] = useState( null );
    const [kaplamaState, setKaplamaState] = useState( null );
    const [ambalajState, setAmbalajState] = useState( null );

    useEffect(() => {
        if (id) {
            listSiparisFiles(id)
                .then(resp => setSiparisFiles(resp.data))
                .catch(err => console.error('Error fetching files:', err));

            getNextStep(id)
                .then(resp => setNextStep(resp.data.nextStep))
                .catch(err => console.error('Error fetching next step:', err));
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            setIsUpdate(true);
            getSiparis(id)
                .then(response => {
                    setFormData({
                        activityId: response.data.activityId,
                        definition: response.data.definition,
                        description: response.data.description,
                        amount: response.data.amount,
                        isOEM: response.data.isOEM,
                        isActive: response.data.isActive,
                        orderNumber: response.data.orderNumber || '',
                        clientOrderNumber: response.data.clientOrderNumber || '',
                        materialNumber: response.data.materialNumber || '',
                        company: response.data.company || '',
                        kaplama: response.data.kaplama || '',
                        quality: response.data.quality || '',
                        patch: response.data.patch || '',
                        material: response.data.material || '',
                        deadline: response.data.deadline ? new Date(response.data.deadline).toISOString().split('T')[0] : '',
                        orderDate: response.data.orderDate ? new Date(response.data.orderDate).toISOString().split('T')[0] : '',
                        state: response.data.state || '',
                        pressState: response.data.pressState,
                        byckState: response.data.byckState,
                        ovalamaState: response.data.ovalamaState,
                        sementasyonState: response.data.sementasyonState,
                        kaplamaState: response.data.kaplamaState,
                        ambalajState: response.data.ambalajState,
                    });
                    setPressState( response.data.pressState );
                    setByckState( response.data.byckState );
                    setOvalamaState( response.data.ovalamaState );
                    setSementasyonState( response.data.sementasyonState );
                    setKaplamaState( response.data.kaplamaState );
                    setAmbalajState( response.data.ambalajState );
                })
                .catch(error => {
                    console.error('Error fetching Siparis:', error);
                    navigate('/siparis');
                });
        }
    }, [id]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: type === 'checkbox' ? checked : value,
        }));
    };

    const handleFileChange = (e) => {
        setFileData(e.target.files[0]);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (readonly) return;  // Prevent form submission if readonly
    
        // Validate required fields
        const requiredFields = {
            definition: 'Ürün Tanımı',
            description: 'Açıklama',
            amount: 'Adet',
            orderDate: 'Sipariş Tarihi',
            deadline: 'Teslim Tarihi'
        };
    
        const missingFields = Object.keys(requiredFields).filter(field => !formData[field]);
    
        if (missingFields.length > 0) {
            const missingLabels = missingFields.map(field => requiredFields[field]).join(', ');
            window.confirm(`Lütfen aşağıdaki gerekli alanları doldurun: ${missingLabels}.`);
            return;
        }
    
        const payload = { ...formData };
    
        (isUpdate ? updateSiparis(id, payload) : createSiparis(payload))
            .then(response => {
                console.log('Siparis saved:', response.data);
                navigate('/siparis');
            })
            .catch(error => {
                console.error('Error saving Siparis:', error);
                setError('Bir hata oluştu, lütfen tekrar deneyin.');
            });
    };
    
    

    const handleNextStep = () => {
        if (!nextStep) return;

        if (!window.confirm(`Gerçekten '${nextStep}' istiyor musunuz?`)) return;
        goNextStep(id)
            .then(() => window.location.reload())
            .catch(error => console.error('Error going to next step:', error));
    };

    const handleFileUpload = () => {
        if (readonly || !fileData) return;  // Prevent file upload if readonly

        const formData = new FormData();
        formData.append('file', fileData);
        formData.append('title', fileData.name);

        createSiparisFile(id, formData)
            .then(response => {
                console.log('File uploaded:', response.data);
                setSiparisFiles([...siparisFiles, response.data]);
                setFileData(null);
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
    };

    const handleFileDelete = (fileId) => {
        if (readonly) return;  // Prevent file deletion if readonly
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

    const handleFileDownload = (fileUrl, fileName) => {
        fetch(fileUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/octet-stream',
            },
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error downloading file:', error);
        });
    };

    return (
        <Container>
            {error && <Typography color="error">{error}</Typography>}
            <Typography variant="h4" gutterBottom>
                {isUpdate ? (readonly ? 'Sipariş Görüntüleme' : 'Sipariş Düzenleme') : 'Sipariş Oluşturma'}
            </Typography>
            {formData?.activityId && (
                <Typography>
                    <Link to={`/siparis-activity/${formData.activityId}`}>Sipariş Aktivitelerine Git</Link>
                </Typography>
            )}
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                {/* Form fields */}
                <TextField
                    fullWidth
                    label="Ürün Tanımı"
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
                    margin="normal"
                    InputProps={{
                        readOnly: true,
                    }}
                />
                <TextField
                    fullWidth
                    label="Müşteri Sipariş Numarası"
                    name="clientOrderNumber"
                    value={formData.clientOrderNumber}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <TextField
                    fullWidth
                    label="Malzeme Numarası"
                    name="materialNumber"
                    value={formData.materialNumber}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <TextField
                    fullWidth
                    label="Şirket"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <FormControl fullWidth margin="normal">
                    <InputLabel>Kaplama</InputLabel>
                    <Select
                        name="kaplama"
                        value={formData.kaplama}
                        onChange={handleChange}
                        disabled={readonly}
                        label="Kaplama"
                    >
                        {Object.keys(KaplamaTypes).map(key => (
                            <MenuItem key={key} value={KaplamaTypes[key]}>
                                {KaplamaTypes[key]}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl fullWidth margin="normal">
                    <InputLabel>Kalite</InputLabel>
                    <Select
                        name="quality"
                        value={formData.quality}
                        onChange={handleChange}
                        disabled={readonly}
                        label="Kalite"
                    >
                        {Object.keys(QualityTypes).map(key => (
                            <MenuItem key={key} value={QualityTypes[key]}>
                                {QualityTypes[key]}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <TextField
                    fullWidth
                    label="Patch"
                    name="patch"
                    value={formData.patch}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <FormControl fullWidth margin="normal">
                    <InputLabel>Malzeme</InputLabel>
                    <Select
                        name="material"
                        value={formData.material}
                        onChange={handleChange}
                        disabled={readonly}
                        label="Malzeme"
                        required
                    >
                        {Object.keys(Materials).map(key => (
                            <MenuItem key={key} value={Materials[key]}>
                                {Materials[key]}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <TextField
                    fullWidth
                    label="Sipariş Tarihi"
                    name="orderDate"
                    type="date"
                    value={formData.orderDate}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                    required
                    InputLabelProps={{ shrink: true }}
                />
                <TextField
                    fullWidth
                    label="Teslim Tarihi"
                    name="deadline"
                    type="date"
                    value={formData.deadline}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                    required
                    InputLabelProps={{ shrink: true }}
                />
                <TextField
                    fullWidth
                    label="Durum"
                    name="state"
                    value={formData.state}
                    onChange={handleChange}
                    margin="normal"
                    InputProps={{
                        readOnly: readonly,
                    }}
                />
                <Box sx={{ mt: 2 }} style={{display: 'flex', flexDirection: 'row'}}>
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Press Durumu</InputLabel>
                        <Select
                            name="pressState"
                            value={formData.pressState}
                            label="Press Durumu"
                            onChange={handleChange}
                        >
                            {ProcessTransitions[ pressState ]?.map(key => (
                                <MenuItem key={key} value={key}>
                                    {key}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Byck Durumu</InputLabel>
                        <Select
                            name="byckState"
                            value={formData.byckState}
                            label="Byck Durumu"
                            onChange={handleChange}
                        >
                            {ProcessTransitions[ byckState ]?.map(key => (
                                <MenuItem key={key} value={key}>
                                    {key}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Ovalama Durumu</InputLabel>
                        <Select
                            name="ovalamaState"
                            value={formData.ovalamaState}
                            label="Ovalama Durumu"
                            onChange={handleChange}
                        >
                            {ProcessTransitions[ ovalamaState ]?.map(key => (
                                <MenuItem key={key} value={key}>
                                    {key}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Sementasyon Durumu</InputLabel>
                        <Select
                            name="sementasyonState"
                            value={formData.sementasyonState}
                            label="Sementasyon Durumu"
                            onChange={handleChange}
                        >
                            {ProcessTransitions[ sementasyonState ]?.map(key => (
                                <MenuItem key={key} value={key}>
                                    {key}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Kaplama Durumu</InputLabel>
                        <Select
                            name="kaplamaState"
                            value={formData.kaplamaState}
                            label="Kaplama Durumu"
                            onChange={handleChange}
                        >
                            {ProcessTransitions[ kaplamaState ]?.map(key => (
                                <MenuItem key={key} value={key}>
                                    {key}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="normal">
                        <InputLabel>Ambalaj Durumu</InputLabel>
                        <Select
                            name="ambalajState"
                            value={formData.ambalajState}
                            label="Ambalaj Durumu"
                            onChange={handleChange}
                        >
                            {ProcessTransitions[ ambalajState ]?.map(key => (
                                <MenuItem key={key} value={key}>
                                    {key}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>
                <Box sx={{ mt: 2 }}>
                    {!readonly && (
                        <Button variant="contained" color="primary" type="submit">
                            {isUpdate ? 'Güncelle' : 'Oluştur'}
                        </Button>
                    )}
                    {isUpdate && nextStep && (
                        <Button variant="contained" color="secondary" onClick={handleNextStep} sx={{ ml: 2 }}>
                            {nextStep}
                        </Button>
                    )}
                </Box>
            </Box>
            <Box sx={{ mt: 3 }}>
                <input type="file" onChange={handleFileChange} />
                <Button variant="contained" onClick={handleFileUpload} disabled={!fileData}>
                    Dosyayı Yükle
                </Button>
                {siparisFiles.length > 0 && (
                    <Box sx={{ mt: 2 }}>
                        {siparisFiles.map(file => (
                            <Box key={file.id} sx={{ mb: 1 }}>
                                <Typography variant="body2">{file.title}</Typography>
                                <Button
                                    variant="text"
                                    color="primary"
                                    onClick={() => handleFileDownload(file.fileUrl, file.title)}
                                >
                                    İndir
                                </Button>
                                { !readonly && (
                                    <Button
                                        variant="text"
                                        color="error"
                                        onClick={() => handleFileDelete(file.id)}
                                    >
                                        Sil
                                    </Button>
                                )}
                            </Box>
                        ))}
                    </Box>
                )}
            </Box>
        </Container>
    );
};

export default SiparisFormPage;
