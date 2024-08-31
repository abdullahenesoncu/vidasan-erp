import React, { useEffect, useRef, useState } from 'react';
import { Timeline } from 'vis-timeline';
import { DataSet } from 'vis-data';
import 'vis-timeline/styles/vis-timeline-graph2d.min.css';
import { fetchMachineLogs } from '../actions/machine';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import { useParams } from 'react-router-dom';

const MachineLogsTimeline = () => {
    const { machineId } = useParams();
    const [logsData, setLogsData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const timelineRef = useRef(null);
    const containerRef = useRef(null);

    useEffect(() => {
        fetchMachineLogs(machineId)
            .then(response => {
                setLogsData(response.data);
                setLoading(false);
            })
            .catch(error => {
                setError(error);
                setLoading(false);
            });
    }, [machineId]);

    useEffect(() => {
        if (logsData && containerRef.current) {
            const items = new DataSet();

            Object.keys(logsData.logs).forEach(machineId => {
                logsData.logs[machineId].forEach((log, index) => {
                    items.add({
                        id: `${machineId}-${index}`,
                        content: `Process: ${log.process}<br>State: ${log.state}`,
                        start: new Date(log.created_at), // Placeholder: Replace with actual start time if available
                        group: machineId,
                    });
                });
            });

            const groups = new DataSet(
                Object.keys(logsData.machineIdToName).map(machineId => ({
                    id: machineId,
                    content: logsData.machineIdToName[machineId],
                }))
            );

            const options = {
                width: '100%',
                height: '400px',
                stack: true,
                zoomMin: 1000,
                zoomMax: 31536000000,
                horizontalScroll: true,
                clickToUse: true,
            };

            timelineRef.current = new Timeline(containerRef.current, items, groups, options);

            return () => {
                if (timelineRef.current) {
                    timelineRef.current.destroy();
                }
            };
        }
    }, [logsData]);

    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error.message}</Alert>;

    return (
        <div>
            <h2>Makine Logları</h2>
            <div ref={containerRef}></div>
        </div>
    );
};

export default MachineLogsTimeline;
