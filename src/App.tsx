import React from 'react';

// TODO: use process.env.NODE_ENV for production or dev API routes

export const App = () => {
  return (
    <div>
      <h2>Santa Claus says</h2>
      <div style={{ color: 'blueviolet', fontSize: '14px' }}>
        Merry Christmas
      </div>
      <div>{process.env.NODE_ENV}</div>
    </div>
  );
};
