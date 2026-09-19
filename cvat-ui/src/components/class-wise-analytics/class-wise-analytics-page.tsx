import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { getCore } from 'cvat-core-wrapper';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface ClassWiseCountResponse {
    status: string;
    total_classes: number;
    data: Record<string, number>;
}

function ClassWiseAnalyticsPage(): JSX.Element {
    const [analytics, setAnalytics] = useState<ClassWiseCountResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const loadAnalytics = async (): Promise<void> => {
        try {
            setError(null);

            const core = getCore();
            const result = await core.analytics.classWiseCount();

            setAnalytics(result);
        } catch (errorData: unknown) {
            setError(errorData instanceof Error ? errorData.message : 'Failed to load analytics');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadAnalytics();

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const websocket = new WebSocket(
            `${protocol}//${window.location.host}/ws/class-wise-analytics/`,
        );

        websocket.onmessage = (event: MessageEvent): void => {
            try {
                const message = JSON.parse(event.data);

                if (message.type === 'class-wise-update') {
                    void loadAnalytics();
                }
            } catch {
                // Ignore malformed WebSocket messages.
            }
        };

        websocket.onerror = (): void => {
            // Initial API data remains available even if WebSocket disconnects.
        };

        return () => {
            websocket.close();
        };
    }, []);

    if (loading) {
        return <div style={{ padding: 24 }}>Loading class-wise analytics...</div>;
    }

    if (error) {
        return <div style={{ padding: 24 }}>Failed to load analytics: {error}</div>;
    }

    const data = analytics?.data || {};

    const chartData = {
        labels: Object.keys(data),
        datasets: [
            {
                label: 'Annotation Count',
                data: Object.values(data),
            },
        ],
    };

    return (
        <div style={{ padding: 24 }}>
            <h1>Class-wise Analytics</h1>
            <p>Total Classes: {analytics?.total_classes || 0}</p>

            {Object.keys(data).length > 0 ? (
                <Bar
                    data={chartData}
                    options={{
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                            },
                            title: {
                                display: true,
                                text: 'Annotations by Class',
                            },
                        },
                    }}
                />
            ) : (
                <p>No annotation data available.</p>
            )}
        </div>
    );
}

export default ClassWiseAnalyticsPage;