import React from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const ContactosGraph = ({ candidatoId, contactos }) => {
  // Nodos: el candidato principal y sus contactos
  const nodes = [
    { id: candidatoId, main: true },
    ...contactos.map(c => ({ id: c.id, main: false }))
  ];
  // Enlaces: del candidato principal a cada contacto
  const links = contactos.map(c => ({
    source: candidatoId,
    target: c.id
  }));

  const graphData = { nodes, links };

  return (
    <div style={{ height: 400, background: '#222', borderRadius: 8 }}>
      <ForceGraph2D
        graphData={graphData}
        nodeAutoColorBy="main"
        nodeLabel={node => node.id}
        linkDirectionalParticles={2}
        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.id;
          const fontSize = node.main ? 18 : 14;
          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.fillStyle = node.main ? '#FFD700' : '#00BFFF';
          ctx.beginPath();
          ctx.arc(node.x, node.y, node.main ? 10 : 7, 0, 2 * Math.PI, false);
          ctx.fill();
          ctx.fillStyle = '#fff';
          ctx.fillText(label, node.x + 12, node.y + 4);
        }}
      />
    </div>
  );
};

export default ContactosGraph;