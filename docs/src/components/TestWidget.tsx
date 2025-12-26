import React from 'react';

export default function TestWidget() {
  return (
    <div
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '200px',
        height: '100px',
        backgroundColor: '#25c2a0',
        color: 'white',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '18px',
        fontWeight: 'bold',
      }}
    >
      TEST WIDGET VISIBLE
    </div>
  );
}
