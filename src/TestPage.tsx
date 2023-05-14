import { Button, Icon, styled } from '@mui/material';
import { Box } from '@mui/system';
import React, { useState } from 'react';

const ButtonRow = styled('div')(`
  padding: 16px;
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
`);

interface TestPageProps {
  apiDomain: string;
}

const TestPage = (props: TestPageProps) => {
  const [testMsg, setTestMsg] = useState('');
  const testApiRead = async () => {
    const resp = await fetch(props.apiDomain + '/api/hello');
    const result = await resp.json();
    setTestMsg(result['message']);
  };
  return (
    <div>
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
    </div>
  );
};

export default TestPage;
