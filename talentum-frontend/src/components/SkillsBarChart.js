import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const SkillsBarChart = ({ candidatos }) => {
  // Contar skills
  const skillCounts = {};
  candidatos.forEach(c => {
    (c.skills_tecnicos || []).forEach(skill => {
      skillCounts[skill] = (skillCounts[skill] || 0) + 1;
    });
  });
  const data = Object.entries(skillCounts).map(([skill, count]) => ({ skill, count }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="skill" />
        <YAxis allowDecimals={false} />
        <Tooltip />
        <Bar dataKey="count" fill="#1976d2" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default SkillsBarChart;