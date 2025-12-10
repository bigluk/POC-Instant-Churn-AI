import React from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

interface ChartPoint {
    date: string;
    ip: number;
}

interface Props {
    data: ChartPoint[];
    userId: string;
}

const UserChart: React.FC<Props> = ({ data, userId }) => {
    return (
        <div className="mt-4">
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={(value: string) => value.slice(0, 5)} />
                    <YAxis />
                    <Tooltip formatter={(value: number) => `${value}%`} />
                    <Line
                        type="monotone"
                        dataKey="ip"
                        stroke="#11710aff"
                        strokeWidth={3}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default UserChart;
