import { Button, Icon, styled } from '@mui/material';
import { Box } from '@mui/system';
import React, { useState } from 'react';

const API_DOMAIN =
  process.env.NODE_ENV === 'development'
    ? 'http://localhost:3000'
    : 'https://dumb-trivia.vercel.app/';

const GlobalWrapper = styled('div')(
  ({ theme }) => `
  color: ${theme.palette.text.primary};
  font-family: ${theme.typography.fontFamily};
`,
);

const ButtonRow = styled('div')(`
  padding: 16px;
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
`);

export const App = () => {
  const [testMsg, setTestMsg] = useState('');
  const testApiRead = async () => {
    const resp = await fetch(API_DOMAIN + '/api/hello');
    const result = await resp.json();
    setTestMsg(result['message']);
  };
  return (
    <GlobalWrapper>
      <Box sx={{ color: 'text.primary', fontSize: 34, fontWeight: 'medium' }}>
        Test that sheets work
      </Box>
      <ButtonRow>
        <Icon>star</Icon>
        <Button variant="contained" disableElevation onClick={testApiRead}>
          Test the thing
        </Button>
        {testMsg && <div>{testMsg}</div>}
      </ButtonRow>
      <div>{process.env.NODE_ENV}</div>
    </GlobalWrapper>
  );
};
